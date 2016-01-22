from flask import Flask

from .database import db


def create_app(cfg):
    """Returns an app of given config"""
    # configure app from the config
    config = get_config(cfg)
    app = Flask(config.PROJECT_NAME)
    app.config.from_object(config)

    # set database for the app
    db.init_app(app)

    return app


def setup_db(app):
    """Initialize database for the app"""
    from .users import models as user_models
    from .sites import models as site_models
    from .pages import models as page_models
    from .schedules import models as schedule_models
    with app.app_context():
        db.create_all()


def get_config(cfg):
    """Returns a config object of given name"""
    if isinstance(cfg, str):
        module = __import__('config', fromlist=[cfg])
        return getattr(module, cfg)
    return cfg
