from components.server.news.models import News


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


def test_news_deletion():
    # TODO: NOT IMPLEMTED YET
    pass


def test_rating_attributes():
    # TODO: NOT IMPLEMTED YET
    pass


def test_rating_creation():
    # TODO: NOT IMPLEMTED YET
    pass


def test_rating_update():
    # TODO: NOT IMPLEMTED YET
    pass


def test_rating_deletion():
    pass
