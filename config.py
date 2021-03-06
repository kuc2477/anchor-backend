from datetime import timedelta
from secret import (
    DB_NAME,
    DB_ENDPOINT,
    DB_PORT,
    DB_USERNAME,
    DB_PASSWORD,
    SECRET_KEY,
    SECRET_SALT,
    MAIL_SERVER,
    MAIL_USERNAME,
    MAIL_PASSWORD
)


class Base(object):
    PROJECT_NAME = 'anchor-backend'
    SERVICE_NAME = 'Anchor'

    # Server Modes
    ADMIN = False
    DEBUG = False
    TESTING = False

    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = \
        'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(
            DB_USERNAME, DB_PASSWORD, DB_ENDPOINT, DB_PORT, DB_NAME
        )

    # Session
    SECRET_SALT = SECRET_SALT
    SECRET_KEY = SECRET_KEY
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # Mail
    MAIL_SERVER = MAIL_SERVER
    MAIL_DEFAULT_SENDER = MAIL_USERNAME
    MAIL_USERNAME = MAIL_USERNAME
    MAIL_PASSWORD = MAIL_PASSWORD
    MAIL_PORT = 465
    MAIL_USE_SSL = True

    # Celery
    CELERY_BROKER_URL = BROKER_URL = 'redis://'
    CELERY_RESULT_BACKEND = 'redis://'
    CELERY_RESULT_ENGINE_OPTIONS = {'echo': False}
    CELERY_REDIRECT_STDOUTS = False
    CELERY_TRACK_STARTED = True

    # Crossbar
    CROSSBAR_REALM = u'anchor'
    CROSSBAR_URL = u'ws://localhost:8080/ws'


class Dev(Base):
    # Mode
    ADMIN = True
    DEBUG = True

    # Crossbar
    CROSSBAR_REALM = u'realm1'
    CROSSBAR_URL = u'wss://demo.crossbar.io/ws'


class Test(Base):
    # Mode
    TESTING = True

    # Database
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class Prod(Base):
    PROPAGATE_EXCEPTIONS = True
