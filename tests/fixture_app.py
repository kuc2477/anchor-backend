import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from config import Test
from app import create_app
from app.extensions import db as database


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
    transaction = connection.begin()

    session_factory = sessionmaker(bind=connection)
    db.session = session = scoped_session(session_factory)

    yield session

    transaction.rollback()
    connection.close()
    session.remove()
