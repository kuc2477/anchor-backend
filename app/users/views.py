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


@users.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    password = request.form['password']
    password_check = request.form['password_check']

    password_ok = password == password_check
    already_exists = User.query.filter_by(email=email).first

    if not password_ok or already_exists:
        abort(400)

@users.route('/confirm', methods=['GET'])
def confirm():
    pass

@users.route('/userinfo', methods=['GET'])
def user_info():
    if current_user.is_authenticated:
        return jsonify({ 'user': current_user.serialized })
    else:
        abort(401)
