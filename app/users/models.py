import validators
from werkzeug import (
    generate_password_hash,
    check_password_hash
)
from marshmallow import (
    Schema as MarshmallowSchema,
    fields
)
from flask.ext.login import UserMixin
from flask.ext.restful.reqparse import RequestParser
from flask.ext.restful import (
    Resource as RESTResource,
    abort
)


from .. import db
from ..utils import classproperty


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(60))

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email.lower()
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def serialized(self):
        schema = self.Schema()
        return schema.dump(self)

    @classproperty
    def registration_parser(cls):
        parser = RequestParser()
        _add_email(parser)
        _add_firstname(parser)
        _add_lastname(parser)
        _add_password(parser)
        _add_password_check(parser)
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

    class ListResource(Resource):

        def post(self):
            args = User.registration_parser.parse_args()

            password_checked = args['password'] == args['password_check']
            already_exists = User.query.filter_by(email=args['email']).first()

            if not password_checked or already_exists:
                abort(400)

            user = User(
                args['firstname'], args['lastname'],
                args['email'], args['password']
            )
            db.session.add(user)
            db.session.commit()
            return user.serialized, 201


# ======================
# Parser argument adders
# ======================

def _add_email(parser):
    def email_type(value):
        if not validators.email(value):
            raise ValueError('Invalid email format')
        return value
    parser.add_argument(
        'email', type=email_type, required=True,
        help='email of ther user'
    )


def _add_firstname(parser):
    parser.add_argument(
        'firstname', type=str, required=True,
        help='firstname of the user'
    )


def _add_lastname(parser):
    parser.add_argument(
        'lastname', type=str, required=True,
        help='lastname of the user'
    )


def _add_password(parser):
    parser.add_argument(
        'password', type=str, required=True,
        help='password of the user'
    )


def _add_password_check(parser):
    parser.add_argument(
        'password_check', type=str, required=True,
        help='password check for correct password registration'
    )
