import os
from datetime import timedelta
from secret import (
    DB_NAME,
    DB_USERNAME,
    DB_PASSWORD,
    SECRET_KEY,
    MAIL_SERVER,
    MAIL_USERNAME,
    MAIL_PASSWORD
)


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
        'postgresql+psycopg2://{0}:{1}@localhost:5432/{2}'.format(
            DB_USERNAME, DB_PASSWORD, DB_NAME
        )

    # Session
    SECRET_KEY = SECRET_KEY
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # Mail
    MAIL_SERVER = MAIL_SERVER
    MAIL_USERNAME = MAIL_USERNAME
    MAIL_PASSWORD = MAIL_PASSWORD
    MAIL_PORT = 465
    MAIL_USE_SSL = True


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
