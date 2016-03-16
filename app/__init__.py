from flask import Flask
from celery import Celery
from news.backends.sqlalchemy import SQLAlchemyBackend
from news.scheduler import Scheduler

from .extensions import (
    db,
    configure_db,
    configure_ma,
    configure_login,
    configure_mail,
    configure_admin,
    register_blueprints
)
from .users.views import bp as users_bp
from .schedules.views import bp as schedules_bp
from .news.views import bp as news_bp
from .users.models import User
from .schedules.models import Schedule
from .news.models import News


def create_app(cfg):
    """Returns an app of given config"""
    # configure app from the config
    config = get_config(cfg)
    app = Flask(config.PROJECT_NAME)
    app.config.from_object(config)

    # configure extensions on app
    configure_db(app)
    configure_ma(app)
    configure_login(app)
    configure_mail(app)

    # configure admin extension only when in admin mode
    if config.ADMIN:
        configure_admin(app)

    # register blueprints
    register_blueprints(app, users_bp, schedules_bp, news_bp)

    return app


def create_celery(app):
    # hook up celery with flask configuration
    celery = Celery(
        app.config['SERVICE_NAME'],
        broker=app.config.get('CELERY_BROKER_URL')
    )
    celery.conf.update(app.config)

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        """Adds support for Flask's app contexts"""
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_news_backend(app):
    return SQLAlchemyBackend(
        bind=db.session,
        owner_class=User,
        schedule_class=Schedule,
        news_class=News
    )


def create_news_scheduler(backend, celery):
    return Scheduler(backend, celery)


def get_config(cfg):
    """Returns a config object of given name"""
    if isinstance(cfg, str):
        module = __import__('config', fromlist=[cfg])
        return getattr(module, cfg)
    return cfg
