from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
)
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from flask.ext.restful import (
    Resource,
)
from news.models.sqlalchemy import (
    create_abc_news, create_news
)
from ..users.models import User
from ..schedules.models import Schedule
from ..utils.restful import PaginatedResource
from ..utils.ma import get_base_schema
from ..extensions import db


# ================
# Models & Schemes
# ================

class ABCNews(create_abc_news(Schedule)):
    @property
    def serialized(self):
        schema = NewsSchema()
        return schema.dump(self).data


News = create_news(create_abc_news(Schedule), db.Model)
NewsSchema = get_base_schema(News)


class Rating(db.Model):
    @declared_attr
    def __table__args(cls):
        return (UniqueConstraint('user_id', 'news_id'),)

    @declared_attr
    def user_id(cls):
        return Column(Integer, ForeignKey(User.id))

    @declared_attr
    def user(cls):
        return relationship(User, backref='ratings')

    @declared_attr
    def news_id(cls):
        return Column(Integer, ForeignKey(News.id))

    @declared_attr
    def news(cls):
        return relationship(News, backref='news_list')

    id = Column(Integer, primary_key=True)
    value = Column(Integer)

    @property
    def serialized(self):
        schema = RatingSchema()
        return schema.dump(self).data


RatingSchema = get_base_schema(Rating)


# =========
# Resources
# =========

class NewsResource(Resource):
    def get(self, id):
        # TODO: NOT IMPLEMTED YET
        pass

    def delete(self, id):
        # TODO: NOT IMPLEMTED YET
        pass

    def put(self, id):
        # TODO: NOT IMPLEMTED YET
        pass


class NewsListResource(PaginatedResource):
    model = News
    schema = NewsSchema


class RatingResource(Resource):
    def get(self, id):
        # TODO: NOT IMPLEMTED YET
        pass

    def delete(self, id):
        # TODO: NOT IMPLEMTED YET
        pass

    def put(self, id):
        # TODO: NOT IMPLEMTED YET
        pass


class RatingListResource(PaginatedResource):
    model = Rating
    schema = RatingSchema

    def post(self):
        # TODO: NOT IMPLEMTED YET
        pass
