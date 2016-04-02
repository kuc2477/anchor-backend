from flask import Flask
from celery import Celery
from .extensions import (
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

    # add support for flask's app context to celery
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery


def get_config(cfg):
    """Returns a config object of given name"""
    if isinstance(cfg, str):
        module = __import__('config', fromlist=[cfg])
        return getattr(module, cfg)
    return cfg
