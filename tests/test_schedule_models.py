from components.server.schedules.models import Schedule
from components.server.users.models import User
from components.server.news.models import News


def test_schedule_creation(session, owner):
    assert(not Schedule.query.all())
    schedule = Schedule(
        name='testname', owner=owner,
        url='http://httpbin.org'
    )
    session.add(schedule)
    session.commit()
    assert(schedule in session)


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


def test_news_creation(session, schedule):
    assert(not News.query.all())
    news = News(
        schedule=schedule,
        url='http://www.naver.com',
        content='fixturecontent'
    )
    session.add(news)
    session.commit()
    assert(news in session)


def test_news_attributes(news, schedule):
    assert(news.id)
    assert(news.url)
    assert(news.schedule == schedule)
    assert(news.content)
