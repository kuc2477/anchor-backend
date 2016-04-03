from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Boolean,
)
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from flask import request
from flask.ext.restful import (
    Resource,
    abort,
)
from flask.ext.login import current_user
from news.models.sqlalchemy import (
    create_abc_news, create_news
)
from .forms import (
    RatingCreateForm,
    RatingUpdateForm,
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


News = create_news(ABCNews, db.Model)
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


class RatingResource(Resource):
    def get(self, id):
        rating = Rating.query.get_or_404(id)
        return rating.serialized

    def delete(self, id):
        rating = Rating.query.get_or_404(id)
        db.session.delete(rating)
        db.session.commit()
        return '', 204

    def put(self, id):
        form = RatingUpdateForm(**request.json)
        form.validate()

        rating = Rating.query.get_or_404(id)
        rating.positive = form.positive.data
        db.session.commit()
        return '', 204


class RatingListResource(PaginatedResource):
    model = Rating
    schema = RatingSchema

    def post(self):
        form = RatingCreateForm(**request.json)
        form.validate()

        # abort if no user data has been delivered either via
        # form data or session.
        if not form.user.data and current_user.is_anonymous:
            abort(400)

        rating = Rating(
            user=form.user.data or current_user,
            news=form.news.data,
            positive=form.positive.data
        )
        db.session.add(rating)
        db.session.commit()
        return rating.serialized, 201
