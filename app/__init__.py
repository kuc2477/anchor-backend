import os
import sys

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy


# Configure application
app = Flask(__name__)
app.config.from_object('config')

# Configure database
db = SQLAlchemy(app)
