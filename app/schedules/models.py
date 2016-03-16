from news.models.sqlalchemy import (
    create_abc_schedule, create_schedule
)
from flask.ext.restful import (
    Resource,
    reqparse
)
from ..utils.ma import JSONTypeCoverter
from ..users.models import User
from ..extensions import (
    db, ma, persister
)


class ABCSchedule(create_abc_schedule(User)):
    @property
    def serialized(self):
        schema = ScheduleSchema()
        return schema.dump(self).data


Schedule = create_schedule(ABCSchedule, db.Model, persister=persister)


class ScheduleSchema(ma.ModelSchema):
    class Meta:
        model = Schedule
        model_converter = JSONTypeCoverter


class ScheduleResource(Resource):
    def get(self, id):
        schedule = Schedule.query.get_or_404(id)
        return schedule.serialized

    def post(self):
        pass

    def delete(self, id):
        schedule = self.query.get(id)
        db.session.delete(schedule)
        return '', 204

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('url')
        parser.add_argument('cycle')
        parser.add_argument('max_dist')
        parser.add_argument('max_depth')
        parser.add_argument('brothers')
        parser.add_argument('blacklist')

        args = parser.parse_args()
        schedule = self.query.get_or_404(id)
        schedule.url = args['url']
        schedule.cycle = args['cycle']
        schedule.max_dist = args['max_dist']
        schedule.max_depth = args['max_depth']
        schedule.brothers = args['brothers']
        schedule.blacklist = args['blacklist']
        db.session.commit()
