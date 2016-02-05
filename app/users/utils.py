from datetime import datetime

from itsdangerous import URLSafeTimedSerializer
from flask import (
    current_app,
    url_for,
    render_template
)

from ..utils import (
    get_service_name,
    send_mail
)


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECRET_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token, salt=current_app.config['SECRET_SALT'],
            max_age=expiration
        )
    except:
        return False
    else:
        return email


def send_confirmation_mail(user):
    # generate token and confirmation url
    token = generate_confirmation_token(user.email)
    url = url_for('users.confirm', token=token, _external=True)

    # generate mail title and template
    subject = '[{0}] Confirm your email account'.format(get_service_name())
    html = render_template(
        'users/confirm_mail.html',
        url=url, date=datetime.now()
    )
    # send confirmation mail
    send_mail(user.email, subject, html)
