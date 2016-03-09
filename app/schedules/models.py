from news.models.sqlalchemy import (
    create_abc_schedule, create_schedule
)
from marshmallow import (
    Schema, 
    fields
)
from flask.ext.restful import (
    Resource,
    reqparse
)
from ..users.models import User
from ..extensions import db


class ABCSchedule(create_abc_schedule(User)):
    @property
    def serialized(self):
        schema = self.Schema()
        return schema.dump(self).data

    class Schema(Schema):
        id = fields.Int()
        url = fields.Url()

    class Resource(Resource):
        def get(self, id):
            schedule = self.query.get_or_404(id)
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
            parser.add_argument

            schedule = self.query.get_or_404(id)
            schedule.url = 


Schedule = create_schedule(ABCSchedule, db.Model)
