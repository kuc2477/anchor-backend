import json
from app.extensions import celery
from app.schedules.models import Schedule


def test_schedule_list_resource_get(schedule, client):
    res = client.get('/api/schedules')
    data = json.loads(res.data.decode('utf-8'))
    assert(all([
        isinstance(d['cycle'], int) and
        isinstance(d['url'], str) and
        isinstance(d['blacklist'], list) and
        isinstance(d['brothers'], list) and
        isinstance(d['owner'], int) and
        isinstance(d['name'], str) and
        isinstance(d['enabled'], bool) and
        isinstance(d['state'], str) and
        (d['max_depth'] is None or isinstance(d['max_depth'], int)) and
        (d['max_dist'] is None or isinstance(d['max_dist'], int))
        for d in data
    ]))


def test_schedule_resource_get(schedule, client):
    res = client.get('/api/schedules/{}'.format(schedule.id))
    data = json.loads(res.data.decode('utf-8'))
    assert(data['id'] == schedule.id)
    assert(data['url'] == schedule.url)
    assert(data['blacklist'] == schedule.blacklist)
    assert(data['brothers'] == schedule.brothers)
    assert(data['enabled'] == schedule.enabled)
    assert(data['state'] == schedule.get_state(celery))
    assert(data['owner'] == schedule.owner.id)
    assert(data['name'] == schedule.name)
    assert(data['max_depth'] == schedule.max_depth)
    assert(data['max_dist'] == schedule.max_dist)


def test_schedule_resource_post(session, client, url, owner):
    assert(not Schedule.query.all())
    payload = {
        'owner': owner.id,
        'name': 'testname',
        'url': url,
    }
    res = client.post(
        '/api/schedules',
        data=json.dumps(payload),
        content_type='application/json'
    )
    assert(res.status_code == 201)
    assert(Schedule.query.filter_by(
        owner_id=payload['owner'],
        name=payload['name'],
        url=payload['url'],
    ).first())


def test_schedule_resource_put(session, schedule, client):
    payload = {
        'id': schedule.id,
        'name': 'testnamechanged',
        'enabled': True,
        'url': 'http://testurlchanged.com',
        'cycle': 123,
        'max_depth': 2,
        'max_dist': 2,
        'brothers': ['http://www.naver.com', 'http://www.daum.net']
    }
    res = client.put(
        '/api/schedules/{}'.format(schedule.id),
        data=json.dumps(payload),
        content_type='application/json'
    )
    updated = Schedule.query.get(schedule.id)

    assert(res.status_code == 200)
    assert(updated.name == payload['name'])
    assert(updated.url == payload['url'])
    assert(updated.enabled)
    assert(updated.cycle == payload['cycle'])
    assert(updated.max_depth == payload['max_depth'])
    assert(updated.max_dist == payload['max_dist'])
    assert(updated.brothers == payload['brothers'])


def test_schedule_resource_delete(session, schedule, client):
    assert(Schedule.query.get(schedule.id))
    res = client.delete('/api/schedules/{}'.format(schedule.id))
    assert(res.status_code == 204)
    assert(not Schedule.query.get(schedule.id))
