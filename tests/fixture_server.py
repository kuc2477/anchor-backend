import pytest
from sqlalchemy.orm import sessionmaker
from config import Test
from components.server import create_app
from components.server.extensions import db as database


@pytest.yield_fixture(scope='session')
def app():
    application = create_app(Test)

    # push new flask app context for multi-thread tests to work
    context = application.app_context()
    context.push()

    yield application

    # pop flask app context and drop database
    context.pop()


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


@pytest.yield_fixture(scope='session')
def db(app):
    database.create_all()
    yield database
    database.drop_all()


@pytest.yield_fixture(scope='function')
def session(db):
    connection = db.engine.connect()
    database.create_scoped_session
    transaction = connection.begin()
    db.session = session = sessionmaker(bind=connection)()

    yield session

    session.close()
    transaction.rollback()
    connection.close()
