import os
from datetime import timedelta


class Base(object):
    # Project name
    PROJECT_NAME = 'anchor-backend'

    # Mode
    ADMIN = False
    DEBUG = False
    TESTING = False

    # Database
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = \
        'postgresql://{username}:{password}@localhost/anchor'.format(
            os.environ.get('ANCHOR_DB_USERNAME'),
            os.environ.get('ANCHOR_DB_PASSWORD')
        )

    # Session
    SECRET_KEY = os.environ.get('ANCHOR_SECRET_KEY', 'BASE_SECRET_KEY')
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)


class Dev(Base):
    # Mode
    ADMIN = True
    DEBUG = True

    # Database
    SQLALCHEMY_ECHO = True


class Test(Base):
    # Mode
    TESTING = True


class Prod(Base):
    pass
