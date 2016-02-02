from flask import (
    Blueprint,
    redirect,
    request,
    jsonify,
)
from flask.ext.login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask.ext.restful import (
    Api,
    abort,
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
        return jsonify({ 'user': user.serialized })
    else:
        abort(401)

@users.route('/logout', methods=['POST'])
def logout():
    serialized = current_user.serialized
    logout_user()
    return jsonify({ 'user': serialized })

@users.route('/userinfo', methods=['GET'])
def user_info():
    if current_user.is_authenticated:
        return jsonify({ 'user': current_user.serialized })
    else:
        abort(401)
