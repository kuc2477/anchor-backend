from flask import Flask

from .extensions import (
    configure_db,
    configure_login,
    configure_mail,
    configure_admin
)
from .users.views import users


def create_app(cfg):
    """Returns an app of given config"""
    # configure app from the config
    config = get_config(cfg)
    app = Flask(config.PROJECT_NAME)
    app.config.from_object(config)

    # configure extensions on app
    configure_db(app)
    configure_login(app)
    configure_mail(app)
    if config.ADMIN:
        configure_admin(app)

    # register blueprints
    register_blueprints(app, users)

    return app


def register_blueprints(app, *blueprints):
    for bp in blueprints:
        app.register_blueprint(bp)


def get_config(cfg):
    """Returns a config object of given name"""
    if isinstance(cfg, str):
        module = __import__('config', fromlist=[cfg])
        return getattr(module, cfg)
    return cfg
