from app.schedules.models import Schedule
from app.users.models import User
from app.extensions import celery


def test_schedule_attributes(schedule):
    assert(schedule.id)
    assert(schedule.name)
    assert(schedule.url)
    assert(isinstance(schedule.owner, User))
    assert(schedule.cycle)
    schedule.max_depth
    schedule.max_dist
    assert(isinstance(schedule.get_state(celery), str))
    assert(isinstance(schedule.brothers, list))
    assert(isinstance(schedule.blacklist, list))
    assert(isinstance(schedule.enabled, bool))


def test_schedule_creation(session, owner):
    assert(not Schedule.query.all())
    schedule = Schedule(
        name='testname', owner=owner,
        url='http://httpbin.org'
    )
    session.add(schedule)
    session.commit()
    assert(schedule in session)


def test_schedule_deletion(session, schedule):
    session.delete(schedule)
    session.commit()
    assert(not Schedule.query.get(schedule.id))


def test_schedule_update(session, schedule):
    schedule.url = 'changedurl'
    schedule.name = 'changedname'
    schedule.enabled = True
    session.commit()
    updated = Schedule.query.get(schedule.id)
    assert(updated.url == 'changedurl')
    assert(updated.name == 'changedname')
    assert(updated.enabled)
