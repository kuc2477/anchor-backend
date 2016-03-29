from wtforms import (
    Form,
    TextField,
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
    email = TextField('Email', [Email()])
    password = PasswordField()


@abort_on_validation_fail
class SignupForm(Form):
    email = TextField('Email', [Email()])
    firstname = TextField('Firstname', [Length(min=2, max=50)])
    lastname = TextField('Lastname', [Length(min=2, max=50)])
    password = PasswordField('Password', [Length(min=6, max=50)])
    password_validation = PasswordField(
        'Password Validation', [EqualTo('password')]
    )
