from components.server.news.models import (
    News,
    Rating
)


def test_news_attributes(news, schedule):
    assert(news.id)
    assert(news.url)
    assert(news.schedule == schedule)
    assert(news.content)


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


def test_news_deletion(session, news):
    session.delete(news)
    session.commit()
    assert(not News.query.get(news.id))


def test_rating_attributes(rating, owner, news):
    assert(isinstance(rating.positive, bool))
    assert(rating.user == owner)
    assert(rating.news == news)


def test_rating_creation(session, owner, news):
    assert(not Rating.query.all())
    r = Rating(user=owner, news=news, positive=True)
    session.add(r)
    session.commit()
    assert(Rating.query.first().user == owner)
    assert(Rating.query.first().news == news)
    assert(Rating.query.first().positive)


def test_rating_update(session, rating):
    original = rating.positive
    rating.positive = not rating.positive
    session.commit()
    assert(Rating.query.get(rating.id).positive != original)


def test_rating_deletion(session, rating):
    session.delete(rating)
    session.commit()
    assert(not Rating.query.get(rating.id))
