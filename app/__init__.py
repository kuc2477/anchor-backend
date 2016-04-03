from flask import Flask
from news.backends.sqlalchemy import SQLAlchemyBackend
from news.scheduler import Scheduler
from .extensions import (
    db, celery, persister,
    configure_db,
    configure_redis,
    configure_celery,
    configure_ma,
    configure_login,
    configure_mail,
    configure_admin,
    register_blueprints
)
from .users.models import User
from .news.models import News
from .schedules.models import Schedule
from .users.views import bp as users_bp
from .schedules.views import bp as schedules_bp
from .news.views import bp as news_bp


def get_config(cfg):
    """Returns a config object of given name"""
    if isinstance(cfg, str):
        module = __import__('config', fromlist=[cfg])
        return getattr(module, cfg)
    return cfg


def create_app(cfg):
    """Returns an app of given config"""
    # configure app from the config
    config = get_config(cfg)
    app = Flask(config.PROJECT_NAME)
    app.config.from_object(config)

    # configure extensions on app
    configure_db(app)
    configure_redis(app)
    configure_celery(app)
    configure_ma(app)
    configure_login(app)
    configure_mail(app)

    # configure admin extension only when in admin mode
    if config.ADMIN:
        configure_admin(app)

    # register blueprints
    register_blueprints(app, users_bp, schedules_bp, news_bp)

    return app


def create_scheduler_backend(app):
    # bind models with app config
    configure_db(app)
    return SQLAlchemyBackend(
        owner_class=User,
        schedule_class=Schedule,
        news_class=News,
        bind=db.session
    )


def create_scheduler(app):
    # configure redis and celery with app config
    configure_redis(app)
    configure_celery(app)
    backend = create_scheduler_backend(app)
    return Scheduler(backend, celery, persister=persister)
