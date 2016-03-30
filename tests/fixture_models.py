import pytest
from components.server.users.models import User
from components.server.schedules.models import Schedule


@pytest.yield_fixture
def owner(request, session):
    u = User(
        email='testemail@test.com',
        firstname='testfirstname',
        lastname='testlastname',
        password='testpassword'
    )
    session.add(u)
    session.commit()
    yield u
    session.delete(u)
    session.commit()


@pytest.yield_fixture
def schedule(session, owner):
    s = Schedule(
        name='fixturename',
        owner=owner,
        url='http://www.naver.com'
    )
    session.add(s)
    session.commit()
    yield s
    session.delete(s)
    session.commit()
