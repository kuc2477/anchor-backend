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
from flask.ext.restful import (
    Resource,
    reqparse
)
from ..utils.ma import JSONTypeCoverter
from ..users.models import User
from ..extensions import (
    db,
    ma,
)


class ABCSchedule(create_abc_schedule(User)):
    def __init__(self, name='', owner=None, url='',
                 cycle=DEFAULT_SCHEDULE_CYCLE,
                 max_dist=DEFAULT_MAX_DIST, max_depth=DEFAULT_MAX_DEPTH,
                 blacklist=DEFAULT_BLACKLIST, brothers=DEFAULT_BROTHERS):
        self.name = name
        super().__init__(owner=owner, url=url, cycle=cycle,
                         max_dist=max_dist, max_depth=max_depth,
                         blacklist=blacklist, brother=brothers)

    def __str__(self):
        return '{}\'s schedule {} {}'.format(
            self.owner.fullname if self.owner else 'Anonymous',
            self.name, self.url)

    name = Column(Text, nullable=False, default='')

    @property
    def serialized(self):
        schema = ScheduleSchema()
        return schema.dump(self).data


Schedule = create_schedule(ABCSchedule, db.Model)


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
