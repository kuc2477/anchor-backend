from flask import Flask

from .extensions import (
    configure_db,
    configure_ma,
    configure_login,
    configure_mail,
    configure_admin
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


def register_blueprints(app, *blueprints):
    [app.register_blueprint(bp) for bp in blueprints]


def get_config(cfg):
    """Returns a config object of given name"""
    if isinstance(cfg, str):
        module = __import__('config', fromlist=[cfg])
        return getattr(module, cfg)
    return cfg
