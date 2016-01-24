from flask import Blueprint
from flask import redirect
from flask import request
from flask.ext.login import (
    login_required,
    login_user,
    logout_user
)
from flask.ext.restful import (
    Api,
    abort
)

from .models import User


# users blueprint
users = Blueprint('users', __name__)
users_api = Api(users)

users_api.add_resource(User.Resource, '/users/<int:id>')
users_api.add_resource(User.ListResource, '/users')


@users.route('/')
@login_required
def index():
    return 'LOGINNED (INDEX PAGE)'


@users.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first_or_404()
    if user.check_password(password):
        login_user(user)
        redirect('/')

    abort(401)


@users.route('/logout', methods=['POST'])
def logout():
    logout_user()
