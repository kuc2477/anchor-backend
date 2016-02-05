import validators
from werkzeug import (
    generate_password_hash,
    check_password_hash
)
from marshmallow import (
    Schema as MarshmallowSchema,
    fields
)
from sqlalchemy.sql import func
from sqlalchemy_utils.types.choice import ChoiceType
from flask.ext.login import UserMixin
from flask.ext.restful.reqparse import RequestParser
from flask.ext.restful import (
    Resource as RESTResource,
    abort
)


from ..extensions import db
from ..utils import classproperty


class User(UserMixin, db.Model):
    ADMIN, USER = (u'ADMIN', u'USER')
    ROLES = [
        (ADMIN, u'Admin'),
        (USER, u'User')
    ]

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    role = db.Column(ChoiceType(ROLES), nullable=False, default=USER)
    registered_on = db.Column(db.DateTime, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    def __init__(self, email='', firstname='', lastname='', password='',
                 role=USER, confirmed=False, confirmed_on=None):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email.lower()
        self.set_password(password)

        self.role = role
        self.registered_on = func.now()
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_active(self):
        return self.confirmed

    @property
    def serialized(self):
        schema = self.Schema()
        return schema.dump(self).data

    @classproperty
    def registration_parser(cls):
        parser = RequestParser()
        _add_email(parser, location='form')
        _add_firstname(parser, location='form')
        _add_lastname(parser, location='form')
        _add_password(parser, location='form')
        _add_password_validation(parser, location='form')
        return parser

    @classproperty
    def update_parser(cls):
        parser = RequestParser()
        _add_firstname(parser)
        _add_lastname(parser)
        return parser

    class Schema(MarshmallowSchema):
        id = fields.Int()
        firstname = fields.Str()
        lastname = fields.Str()
        confirmed = fields.Bool()

    class Resource(RESTResource):
        def get(self, id):
            user = User.query.get_or_404(id)
            return user.serialized

        def delete(self, id):
            user = User.query.get(id)
            db.session.delete(user)
            return '', 204

        def put(self, id):
            args = User.update_parser.parse_args()
            user = User.query.get_or_404(id)
            user.firstname = args['firstname']
            user.lastname = args['lastname']
            db.session.commit()
            return user.serialized


# ======================
# Parser argument adders
# ======================

def _add_email(parser, **kwargs):
    def email_type(value):
        if not validators.email(value):
            raise ValueError('Invalid email format')
        return value

    parser.add_argument(
        'email', type=email_type, required=True,
        help='email of ther user', **kwargs
    )


def _add_firstname(parser, **kwargs):
    parser.add_argument(
        'firstname', type=str, required=True,
        help='firstname of the user', **kwargs
    )


def _add_lastname(parser, **kwargs):
    parser.add_argument(
        'lastname', type=str, required=True,
        help='lastname of the user', **kwargs
    )


def _add_password(parser, **kwargs):
    parser.add_argument(
        'password', type=str, required=True,
        help='password of the user', **kwargs
    )


def _add_password_validation(parser, **kwargs):
    parser.add_argument(
        'password_validation', type=str, required=True,
        help='password validation for correct password registration', **kwargs
    )
