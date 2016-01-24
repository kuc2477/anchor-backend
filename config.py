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
        'sqlite:////tmp/%s_base.sqlite' % PROJECT_NAME

    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)


class Dev(Base):
    # Mode
    ADMIN = True
    DEBUG = True

    # Database
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = \
        'sqlite:////tmp/%s_dev.sqlite' % Base.PROJECT_NAME


class Test(Base):
    # Mode
    TESTING = True

    # Database
    SQLALCHEMY_DATABASE_URI = \
        'sqlite:////tmp/%s_test.sqlite' % Base.PROJECT_NAME


class Prod(Base):
    pass
