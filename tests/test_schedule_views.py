import json
from app.extensions import celery
from app.schedules.models import Schedule


def test_schedule_list_resource_get(schedule, client):
    res = client.get('/api/schedules')
    data = json.loads(res.data.decode('utf-8'))
    assert(all([
        isinstance(d['cycle'], int) and
        isinstance(d['url'], str) and
        isinstance(d['owner'], int) and
        isinstance(d['name'], str) and
        isinstance(d['enabled'], bool) and
        isinstance(d['state'], str) and
        isinstance(d['options'], dict)
        for d in data
    ]))


def test_schedule_resource_get(schedule, client):
    res = client.get('/api/schedules/{}'.format(schedule.id))
    data = json.loads(res.data.decode('utf-8'))
    options = data['options']
    assert(data['id'] == schedule.id)
    assert(data['url'] == schedule.url)
    assert(options['ext_blacklist'] == schedule.options['ext_blacklist'])
    assert(options['url_whitelist'] == schedule.options['url_whitelist'])
    assert(data['enabled'] == schedule.enabled)
    assert(data['state'] == schedule.get_state(celery))
    assert(data['owner'] == schedule.owner.id)
    assert(data['name'] == schedule.name)
    assert(options['max_dist'] == schedule.options['max_dist'])
    assert(options['max_visit'] == schedule.options['max_visit'])


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
    options = {
        'max_visit': 300,
        'max_dist': 2,
        'url_whitelist': ['http://www.naver.com', 'http://www.daum.net'],
    }
    payload = {
        'id': schedule.id,
        'name': 'testnamechanged',
        'enabled': True,
        'url': 'http://testurlchanged.com',
        'cycle': 123,
        'options': options
    }

    response = client.put(
        '/api/schedules/{}'.format(schedule.id),
        data=json.dumps(payload),
        content_type='application/json'
    )
    updated = Schedule.query.get(schedule.id)

    assert(response.status_code == 200)
    assert(updated.name == payload['name'])
    assert(updated.url == payload['url'])
    assert(updated.enabled)
    assert(updated.cycle == payload['cycle'])
    assert(updated.options['max_visit'] == options['max_visit'])
    assert(updated.options['max_dist'] == options['max_dist'])
    assert(updated.options['url_whitelist'] == options['url_whitelist'])


def test_schedule_resource_delete(session, schedule, client):
    assert(Schedule.query.get(schedule.id))
    res = client.delete('/api/schedules/{}'.format(schedule.id))
    assert(res.status_code == 204)
    assert(not Schedule.query.get(schedule.id))
