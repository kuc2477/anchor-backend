from flask import request
from flask.ext.login import current_user
from flask.ext.restful import (
    Resource,
    abort
)
from .models import (
    Schedule,
    ScheduleSchema,
)
from .forms import (
    ScheduleCreateForm,
    ScheduleUpdateForm,
)
from ..utils.restful import PaginatedResource
from ..extensions import db


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
        schedule.options = form.options.data
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
            options=form.options.data,
        )
        db.session.add(schedule)
        db.session.commit()
        return schedule.serialized, 201
