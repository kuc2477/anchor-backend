from marshmallow import fields
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Boolean,
)
from sqlalchemy import sql
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from flask.ext.restful import Resource
from flask.ext.login import current_user
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
        schema = NewsSchema(exclude=['content'])
        return schema.dump(self).data

    @property
    def current_user_rating(self):
        if current_user.is_anonymous:
            return None
        try:
            rating = [r for r in self.ratings if r.user == self.owner][0]
            return rating.positive
        except IndexError:
            return None


News = create_news(ABCNews, db.Model)


class NewsSchema(get_base_schema(News)):
    title = fields.String()
    description = fields.String()
    image = fields.String()
    current_user_rating = fields.Boolean(allow_none=True)


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
        return relationship(News, backref='ratings')

    def __init__(self, user, news, positive=True):
        # support both foreign key and model instance
        isinstance(user, int) and setattr(self, 'user_id', user)
        not isinstance(user, int) and setattr(self, 'user', user)
        isinstance(news, int) and setattr(self, 'news_id', news)
        not isinstance(news, int) and setattr(self, 'news', news)
        self.positive = positive

    id = Column(Integer, primary_key=True)
    positive = Column(Boolean, default=True)

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
        news = News.query.get_or_404(id)
        return news.serialized

    def delete(self, id):
        news = Schedule.query.get_or_404(id)
        db.session.delete(news)
        db.session.commit()
        return '', 204


class NewsListResource(PaginatedResource):
    model = News
    schema = NewsSchema

    def get_query(self):
        if current_user.is_anonymous:
            return News.query.filter(sql.false())
        else:
            return self.model.query.join(Schedule).filter(
                Schedule.owner_id == current_user.id
            )
