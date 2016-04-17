import os
import config
from flask import Flask
from .extensions import (
    configure_db,
    configure_scheduler,
    configure_redis,
    configure_celery,
    configure_ma,
    configure_login,
    configure_mail,
    configure_admin,
    register_blueprints
)
from .users.views import bp as users_bp
from .users.models import User
from .schedules.views import bp as schedules_bp
from .schedules.models import Schedule
from .news.views import bp as news_bp
from .news.models import News


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
    configure_scheduler(
        app,
        user_model=User,
        schedule_model=Schedule,
        news_model=News
    )
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


def create_app_from_env():
    try:
        config_name = os.environ['ANCHOR_CONFIG'].title()
    except KeyError:
        config_name = 'Dev'

    return create_app(getattr(config, config_name))
