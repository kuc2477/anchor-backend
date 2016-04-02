import pytest
from components.server.users.models import User
from components.server.schedules.models import Schedule
from components.server.news.models import (
    News,
    Rating
)


@pytest.fixture
def owner(request, session):
    u = User(
        email='testemail@test.com',
        firstname='testfirstname',
        lastname='testlastname',
        password='testpassword'
    )
    session.add(u)
    session.commit()
    return u


@pytest.fixture
def schedule(session, owner):
    s = Schedule(
        name='fixturename',
        owner=owner,
        url='http://www.naver.com'
    )
    session.add(s)
    session.commit()
    return s


@pytest.fixture
def news(session, schedule):
    n = News(
        schedule=schedule,
        url='http://www.naver.com',
        content='fixturecontent'
    )
    session.add(n)
    session.commit()
    return n

@pytest.fixture
def rating(session, owner, news):
    r = Rating(
        user=owner,
        news=news,
        positive=True,
    )
    session.add(r)
    session.commit()
    return r
