from marshmallow import fields
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Boolean,
)
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr
from flask.ext.login import current_user
from news.models.sqlalchemy import (
    create_news_abc, create_news
)
from ..users.models import User
from ..schedules.models import Schedule
from ..utils.ma import get_base_schema
from ..extensions import db


class NewsABC(create_news_abc(Schedule)):
    @property
    def serialized(self):
        schema = NewsSchema(exclude=['content'])
        return schema.dump(self).data

    @property
    def words(self):
        title_tokens = self.title.split() if self.title else []
        summary_tokens = self.summary.split() if self.summary else []
        return title_tokens + summary_tokens

    @property
    def user_rating(self):
        return self.get_rating(user=current_user)

    def get_rating(self, user=None):
        user = user or current_user
        if user.is_anonymous:
            return None
        try:
            rating = [r for r in self.ratings if r.user == self.owner][0]
            return rating.positive
        except IndexError:
            return None


News = create_news(NewsABC, db.Model)


class NewsSchema(get_base_schema(News)):
    user_rating = fields.Boolean(allow_none=True)

    class Meta:
        exclude = ('content',)


class Rating(db.Model):
    @declared_attr
    def __table__args(cls):
        return (UniqueConstraint('user_id', 'news_id'),)

    @declared_attr
    def user_id(cls):
        return Column(Integer, ForeignKey(User.id))

    @declared_attr
    def user(cls):
        return relationship(User, backref=backref(
            'ratings',
            cascade='delete-orphan, all'
        ))

    @declared_attr
    def news_id(cls):
        return Column(Integer, ForeignKey(News.id))

    @declared_attr
    def news(cls):
        return relationship(News, backref=backref(
            'ratings',
            cascade='delete-orphan, all'
        ))

    def __init__(self, user, news, positive=True):
        self.user = user
        self.news = news
        self.positive = positive

    id = Column(Integer, primary_key=True)
    positive = Column(Boolean, default=True)

    @property
    def serialized(self):
        schema = RatingSchema()
        return schema.dump(self).data


RatingSchema = get_base_schema(Rating)
