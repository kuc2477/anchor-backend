from flask import Blueprint
from flask.ext.login import login_required

# users app blueprint
users = Blueprint('users', __name__)


@users.route('/')
@login_required
def index():
    return 'INDEX PAGE NOT IMPLEMENTED YET'


@users.route('/login')
def login():
    return 'LOGIN API NOT IMPLEMENTED YET'


@users.route('/logout')
def logout():
    return 'LOGOUT API NOT IMPLEMENTED YET'
