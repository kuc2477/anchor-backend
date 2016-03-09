from datetime import datetime
from flask import (
    Blueprint,
    request,
    jsonify,
    render_template
)
from flask.ext.login import (
    current_user,
    login_user,
    logout_user,
)
from flask.ext.restful import (
    Api,
    abort,
)
from ..extensions import db
from .models import (
    User,
    UserResource
)
from .forms import (
    AuthenticationForm,
    SignupForm,
)
from .utils import (
    send_confirmation_mail,
    confirm_token,
    get_user_or_404,
    get_user,
)
from ..utils.http import error


# users blueprint
users = Blueprint('users', __name__, template_folder='templates')
users_api = Api(users)
users_api.add_resource(UserResource, '/users/<int:id>')


@users.route('/login', methods=['POST'])
def login():
    form = AuthenticationForm(request.form)
    form.validate()

    user = User.query.filter_by(email=form.email.data).first_or_404()
    if not user.check_password(form.password.data):
        abort(401)

    if login_user(user):
        return jsonify({'user': user.serialized})
    else:
        return error('User account has not been confirmed yet',
                     401, email=user.email)


@users.route('/logout', methods=['POST'])
def logout():
    serialized = current_user.serialized
    logout_user()
    return jsonify({'user': serialized})


@users.route('/signup', methods=['POST'])
def signup():
    form = SignupForm(request.form)
    form.validate()

    if get_user(form.email.data):
        return error('Email already exists')

    # validation passed. register the user
    user = User(form.email.data, form.firstname.data, form.lastname.data,
                form.password.data)
    db.session.add(user)
    db.session.commit()

    # send confirmation email and login the user
    send_confirmation_mail(user)
    login_user(user)

    return jsonify({'email': user.email}), 201


@users.route('/resend', methods=['POST'])
def resend():
    user = get_user_or_404(request.form['email'])

    if not user.confirmed:
        send_confirmation_mail(user)
        return '', 201

    else:
        return error('Account is already confirmed')


@users.route('/confirm/<token>', methods=['GET'])
def confirm(token):
    try:
        email = confirm_token(token)
    except:
        # confimation token expired
        return render_template(
            'users/confirm_mail_expired',
            date=datetime.now()
        )
    else:
        # already confirmed
        user = get_user_or_404(email)
        if user.confirmed:
            return render_template(
                'users/already_confirmed.html',
                date=datetime.now()
            )
        # confirmed
        else:
            user.confirmed = True
            user.confirmed_on = datetime.utcnow()
            db.session.commit()
            return render_template(
                'users/confirmed.html',
                date=datetime.now()
            )


@users.route('/userinfo', methods=['GET'])
def userinfo():
    if current_user.is_authenticated:
        return jsonify({'user': current_user.serialized})
    else:
        abort(401)
