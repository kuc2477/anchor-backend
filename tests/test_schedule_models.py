from components.server.schedules.models import Schedule
from components.server.users.models import User


def test_schedule_attributes(schedule):
    assert(schedule.id)
    assert(schedule.name)
    assert(schedule.url)
    assert(isinstance(schedule.owner, User))
    assert(schedule.cycle)
    schedule.max_depth
    schedule.max_dist
    assert(isinstance(schedule.brothers, list))
    assert(isinstance(schedule.blacklist, list))


def test_schedule_creation(session, owner):
    assert(not Schedule.query.all())
    schedule = Schedule(
        name='testname', owner=owner,
        url='http://httpbin.org'
    )
    session.add(schedule)
    session.commit()
    assert(schedule in session)


def test_schedule_deletion():
    # TODO: NOT IMPLEMTED YET
    pass


def test_schedule_update():
    # TODO: NOT IMPLEMTED YET
    pass
