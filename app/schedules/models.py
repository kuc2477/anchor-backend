from marshmallow import fields
from sqlalchemy import (
    Column, Text
)
from news.models.sqlalchemy import (
    create_schedule_abc, create_schedule
)
from ..utils.ma import get_base_schema
from ..users.models import User
from ..extensions import (
    db, celery, persister
)


class ScheduleABC(create_schedule_abc(User)):
    def __init__(self, name='', *args, **kwargs):
        self.name = name
        super().__init__(*args, **kwargs)

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


Schedule = create_schedule(ScheduleABC, db.Model, persister=persister)


class ScheduleSchema(get_base_schema(Schedule, json_field='dict')):
    state = fields.Method('get_state')

    def get_state(self, schedule):
        return schedule.get_state(celery)
