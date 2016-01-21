import os
import sys

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

from .database import db_session


# Configure application
app = Flask(__name__)
app.config.from_object('config')

# Configure database
db = SQLAlchemy(app)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
