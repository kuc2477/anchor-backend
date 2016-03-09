from news.models.sqlalchemy import (
    create_abc_news, create_news
)
from flask.ext.restful import (
    Resource,
)
from ..schedules.models import Schedule
from ..extensions import (
    db,
    ma,
)


class ABCNews(create_abc_news(Schedule)):
    @property
    def serialized(self):
        schema = NewsSchema()
        return schema.dump(self).data


News = create_news(create_abc_news(Schedule), db.Model)


class NewsSchema(ma.ModelSchema):
    class meta:
        model = News


class NewsResource(Resource):
    def get(self, id):
        pass

    def post(self):
        pass

    def delete(self, id):
        pass

    def put(self, id):
        pass
