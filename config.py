import os
from datetime import timedelta

from SECRET import (
    ANCHOR_DB_USERNAME,
    ANCHOR_DB_PASSWORD,
    SECRET_KEY
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
        'postgresql+psycopg2://{0}:{1}@localhost:5432/anchor'.format(
            ANCHOR_DB_USERNAME,
            ANCHOR_DB_PASSWORD
        )

    # Session
    SECRET_KEY = SECRET_KEY
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
