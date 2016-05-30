import pytest
from app.users.models import User
from app.schedules.models import Schedule
from app.news.models import (
    News,
    Rating
)


@pytest.fixture(scope='function')
def owner(request, session):
    u = User(
        email='testemail@test.com',
        firstname='testfirstname',
        lastname='testlastname',
        password='testpassword'
    )
    session.add(u)
    session.commit()

    def teardown():
        session.delete(u)
        session.commit()

    request.addfinalizer(teardown)
    return u


@pytest.fixture(scope='function')
def schedule(request, session, owner):
    s = Schedule(
        name='fixturename',
        owner=owner,
        url='http://www.naver.com'
    )
    session.add(s)
    session.commit()

    def teardown():
        session.delete(s)
        session.commit()

    request.addfinalizer(teardown)
    return s


@pytest.fixture(scope='function')
def news(request, session, schedule):
    n = News(
        schedule=schedule,
        url='http://www.naver.com',
        title='fixturetitle',
        author='fixtureauthor',
        content='fixturecontent',
        summary='fixturesummary'
    )
    session.add(n)
    session.commit()

    def teardown():
        session.delete(n)
        session.commit()

    request.addfinalizer(teardown)
    return n


@pytest.fixture(scope='function')
def rating(request, session, owner, news):
    r = Rating(
        user=owner,
        news=news,
        positive=True,
    )
    session.add(r)
    session.commit()

    def teardown():
        session.delete(r)
        session.commit()
    request.addfinalizer(teardown)
    return r
