from flask import Flask


def create_app(cfg):
    # configure app from the config
    config = get_config(cfg)
    app = Flask(config.PROJECT_NAME)
    app.config.from_object(config)

    # set database for the app
    from .database import db
    db.init_app(app)

    return app


def get_config(cfg):
    if isinstance(cfg, str):
        module = __import__('config', fromlist=[cfg])
        return getattr(module, cfg)
    return cfg
