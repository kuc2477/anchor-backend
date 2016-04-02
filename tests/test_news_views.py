import json
from components.server.news.models import Rating


def test_news_list_resource_get(news, client):
    res = client.get('/api/news')
    data = json.loads(res.data.decode('utf-8'))
    assert(all([
        isinstance(d['schedule'], int) and
        isinstance(d['content'], str) and
        isinstance(d['url'], str)
        for d in data
    ]))


def test_news_resource_get(news, client):
    res = client.get('/api/news/{}'.format(news.id))
    data = json.loads(res.data.decode('utf-8'))
    assert(data['id'] == news.id)
    assert(data['content'] == news.content)
    assert(data['url'] == news.url)
    assert(data['schedule'] == news.schedule.id)
    assert(data['src'] == (news.src.id if news.src else news.src))


def test_rating_list_resource_get(rating, client):
    res = client.get('/api/ratings')
    data = json.loads(res.data.decode('utf-8'))
    assert(all([
        isinstance(d['user'], int) and
        isinstance(d['news'], int) and
        isinstance(d['positive'], bool)
        for d in data
    ]))


def test_rating_resource_get(rating, client):
    res = client.get('/api/ratings/{}'.format(rating.id))
    data = json.loads(res.data.decode('utf-8'))
    assert(data['id'] == rating.id)
    assert(data['positive'] == rating.positive)
    assert(data['news'] == rating.news.id)
    assert(data['user'] == rating.user.id)


def test_rating_resource_post(session, client, owner, news):
    assert(not Rating.query.all())
    payload = {
        'user': owner.id,
        'news': news.id,
        'positive': True
    }
    res = client.post(
        '/api/ratings',
        data=json.dumps(payload),
        content_type='application/json'
    )
    assert(res.status_code == 201)
    assert(Rating.query.filter_by(
        user_id=payload['user'],
        news_id=payload['news'],
        positive=payload['positive'],
    ).first())


def test_rating_resource_put(session, client, rating):
    original = rating.positive
    payload = {'positive': not rating.positive}
    res = client.put(
        '/api/ratings/{}'.format(rating.id),
        data=json.dumps(payload),
        content_type='application/json'
    )
    assert(res.status_code == 204)
    assert(Rating.query.get(rating.id).positive == payload['positive'])


def test_rating_resource_delete(session, client, rating):
    assert(Rating.query.get(rating.id))
    client.delete('/api/ratings/{}'.format(rating.id))
    assert(not Rating.query.get(rating.id))
