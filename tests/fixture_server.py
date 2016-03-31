import pytest
from config import Test
from components.server import create_app
from components.server.extensions import db as database


@pytest.yield_fixture(scope='session')
def app():
    application = create_app(Test)

    # push new flask app context for multi-thread tests to work
    context = application.app_context()
    context.push()
    database.create_all()

    yield application

    # pop flask app context and drop database
    database.drop_all()
    context.pop()


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


@pytest.fixture(scope='session')
def db(app):
    # return database created within app context
    return database


@pytest.yield_fixture(scope='function')
def session(db):
    connection = db.engine.connect()
    transaction = connection.begin()

    test_session_options = dict(bind=connection, binds={})
    test_session = db.create_scoped_session(options=test_session_options)
    db.session = test_session

    yield test_session

    transaction.rollback()
    connection.close()
    test_session.remove()
