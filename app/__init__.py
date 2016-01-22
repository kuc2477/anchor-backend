import os
import sys

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

from .database import db_session


def create_app(config):
    app = Flask(config.PROJECT_NAME)
    app.config.from_object(config)
    return app, SQLAlchemy(app)

def getconfig(name):
    module = __import__('config', fromlist=[name])
    return getattr(module, name)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
