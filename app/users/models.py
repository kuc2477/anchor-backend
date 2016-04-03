from werkzeug import (
    generate_password_hash,
    check_password_hash
)
from sqlalchemy.sql import func
from sqlalchemy_utils.types.choice import ChoiceType
from flask.ext.login import UserMixin
from flask.ext.restful import (
    Resource,
    reqparse
)
from ..extensions import (
    db,
    ma
)


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

    def __str__(self):
        return '{} - {}'.format(self.fullname, self.email)

    @property
    def is_active(self):
        return self.confirmed

    @property
    def serialized(self):
        schema = UserSchema()
        return schema.dump(self).data

    @property
    def fullname(self):
        return '{} {}'.format(self.firstname, self.lastname)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User


class UserResource(Resource):
        def get(self, id):
            user = User.query.get_or_404(id)
            return user.serialized

        def delete(self, id):
            user = User.query.get(id)
            db.session.delete(user)
            return '', 204

        def put(self, id):
            parser = reqparse.RequestParser()
            parser.add_argument('firstname')
            parser.add_argument('lastname')
            args = parser.parse_args()

            user = User.query.get_or_404(id)
            user.firstname = args['firstname']
            user.lastname = args['lastname']
            db.session.commit()
            return user.serialized
