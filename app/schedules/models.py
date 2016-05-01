from marshmallow import fields
from sqlalchemy import (
    Column, Text
)
from news.models.sqlalchemy import (
    create_abc_schedule, create_schedule
)
from news.constants import (
    DEFAULT_SCHEDULE_CYCLE,
    DEFAULT_MAX_DIST,
    DEFAULT_MAX_DEPTH,
    DEFAULT_BLACKLIST,
    DEFAULT_BROTHERS
)
from flask import request
from flask.ext.restful import (
    Resource,
    abort
)
from .forms import (
    ScheduleCreateForm,
    ScheduleUpdateForm,
)
from flask.ext.login import current_user
from ..utils.ma import get_base_schema
from ..utils.restful import PaginatedResource
from ..users.models import User
from ..extensions import (
    db, celery, persister
)


# ==============
# Model & Schema
# ==============

class ABCSchedule(create_abc_schedule(User)):
    def __init__(self, name='', owner=None, url='', enabled=False,
                 cycle=DEFAULT_SCHEDULE_CYCLE,
                 max_dist=DEFAULT_MAX_DIST, max_depth=DEFAULT_MAX_DEPTH,
                 blacklist=DEFAULT_BLACKLIST, brothers=DEFAULT_BROTHERS):
        self.name = name
        super().__init__(owner=owner, url=url, cycle=cycle, enabled=enabled,
                         max_dist=max_dist, max_depth=max_depth,
                         blacklist=blacklist, brothers=brothers)

    def __str__(self):
        return '{}\'s schedule {} {}'.format(
            self.owner.fullname if self.owner else 'Anonymous',
            self.name, self.url)

    name = Column(Text, nullable=False, default='')

    @property
    def serialized(self):
        schema = ScheduleSchema()
        return schema.dump(self).data

    @property
    def state(self):
        return self.get_state(celery)


Schedule = create_schedule(ABCSchedule, db.Model, persister=persister)


class ScheduleSchema(get_base_schema(Schedule)):
    state = fields.Method('get_state')

    def get_state(self, schedule):
        return schedule.get_state(celery)


# =========
# Resources
# =========

class ScheduleResource(Resource):
    def get(self, id):
        schedule = Schedule.query.get_or_404(id)
        return schedule.serialized

    def delete(self, id):
        schedule = Schedule.query.get(id)
        db.session.delete(schedule)
        db.session.commit()
        return '', 204

    def put(self, id):
        form = ScheduleUpdateForm(**request.json)
        form.validate()

        schedule = Schedule.query.get_or_404(form.id.data)
        schedule.enabled = form.enabled.data
        schedule.name = form.name.data
        schedule.url = form.url.data
        schedule.cycle = form.cycle.data
        schedule.enabled = form.enabled.data
        schedule.max_dist = form.max_dist.data
        schedule.max_depth = form.max_depth.data
        schedule.brothers = form.brothers.data
        schedule.blacklist = form.blacklist.data
        db.session.commit()
        return schedule.serialized, 200


class ScheduleListResource(PaginatedResource):
    model = Schedule
    schema = ScheduleSchema

    def post(self):
        form = ScheduleCreateForm(**request.json)
        form.validate()

        if not form.owner.data and current_user.is_anonymous:
            abort(400)

        schedule = Schedule(
            owner=form.owner.data or current_user,
            name=form.name.data,
            url=form.url.data,
            cycle=form.cycle.data,
            max_depth=form.max_depth.data,
            max_dist=form.max_dist.data,
            brothers=form.brothers.data,
            blacklist=form.blacklist.data
        )
        db.session.add(schedule)
        db.session.commit()
        return schedule.serialized, 201
