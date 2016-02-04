from datetime import datetime
from sqlalchemy.sql import func
from flask import (
    Blueprint,
    request,
    jsonify,
    render_template,
    url_for
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
from .utils import generate_confirmation_token
from ..utils import send_mail


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


@users.route('/register', methods=['POST'])
def register():
    args = User.registration_parser.parse_args()

    email = args['email']
    firstname = args['firstname']
    lastname = args['lastname']
    password = args['password']
    password_check = args['password_check']

    password_ok = password == password_check
    already_exists = User.query.filter_by(email=email).first

    if not password_ok or already_exists:
        abort(400)

    # validation passed. register the user
    user = User(firstname, lastname, password)
    db.session.add(user)
    db.session.commit()

    # generate confirmation token and email
    token = generate_confirmation_token(user.email)
    url = url_for('users.confirm', token=token, _external=True)
    html = render_template('users/confirm_email.html', 
                           url=url, date=datetime.now())
    subject = '[Anchor] Confirm your email account'

    # send confirmation email and login the user
    send_mail(user.email, subject, html)
    login_user(user)

    return jsonify({'user': user.serialized}), 201


@users.route('/confirm/<token>', methods=['GET'])
@login_required
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
