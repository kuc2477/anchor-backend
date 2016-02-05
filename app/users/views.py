from datetime import datetime
from flask import (
    Blueprint,
    request,
    jsonify,
    current_app,
    render_template
)
from flask.ext.login import (
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask.ext.restful import (
    Api,
    abort,
)

from ..extensions import db
from .models import User
from .utils import send_confirmation_mail


# users blueprint
users = Blueprint('users', __name__, template_folder='templates')
users_api = Api(users)
users_api.add_resource(User.Resource, '/users/<int:id>')


@users.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first_or_404()

    if user.check_password(password):
        if login_user(user):
            return jsonify({'user': user.serialized})
        else:
            reason = 'User account has not been confirmed yet'
            return jsonify({'reason':reason}), 401
    else:
        abort(401)


@users.route('/logout', methods=['POST'])
def logout():
    serialized = current_user.serialized
    logout_user()
    return jsonify({'user': serialized})


@users.route('/signup', methods=['POST'])
def signup():
    args = User.registration_parser.parse_args(request)

    email = args['email']
    firstname = args['firstname']
    lastname = args['lastname']
    password = args['password']
    password_validation = args['password_validation']

    password_ok = password == password_validation
    already_exists = User.query.filter_by(email=email).first()

    if not password_ok or already_exists:
        reason = 'Password validation failed' if not password_ok else \
            'Email already exists'

        return jsonify({'reason': reason}), 400

    # validation passed. register the user
    user = User(email, firstname, lastname, password)
    db.session.add(user)
    db.session.commit()

    # send confirmation email and login the user
    send_confirmation_mail(user)
    login_user(user)

    return jsonify({'email': user.email}), 201


@users.route('/confirm/<token>', methods=['GET'])
def confirm(token):
    try:
        email = confirm_token(token)
    except:
        reason = 'The confirmation link is invalid or has expired'
        return jsonify({'reason': reason}), 401

    user = User.query.filter_by(email=email).first_or_404()

    if user.confirmed:
        message = 'The account has already been confirmed. Please login.'
        return jsonify({'message': message}), 400
    else:
        user.confirmed = True
        user.confirmed_on = func.now()
        db.session.commit()
        return ('', 204)

@users.route('/userinfo', methods=['GET'])
def user_info():
    if current_user.is_authenticated:
        return jsonify({'user': current_user.serialized})
    else:
        abort(401)
