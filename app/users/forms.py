from wtforms import (
    Form,
    StringField,
    PasswordField,
)
from wtforms.validators import (
    Email,
    Length,
    EqualTo,
)
from ..utils.form import abort_on_validation_fail


@abort_on_validation_fail
class AuthenticationForm(Form):
    email = StringField('Email', [Email()])
    password = PasswordField('Password')


@abort_on_validation_fail
class SignupForm(Form):
    email = StringField('Email', [Email()])
    firstname = StringField('Firstname', [Length(min=2, max=50)])
    lastname = StringField('Lastname', [Length(min=2, max=50)])
    password = PasswordField('Password', [Length(min=6, max=50)])
    password_validation = PasswordField(
        'Password Validation', [EqualTo('password')]
    )
