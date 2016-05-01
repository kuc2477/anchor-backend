from collections import Counter
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    DateTime
)
from sqlalchemy_utils.types import JSONType
from ..users.models import User
from ..news.models import News
from ..extensions import db
from ..constants import (
    DEFAULT_NEWS_SIZE, 
    DEFAULT_CORPUS_SIZE,
)


class Corpus(db.Model):

    id = Column(Integer, primary_key=True)
    words = Column(JSONType, default=[], nullable=False)
    created = Column(DateTime, default=datetime.now)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, news_list=None, size=DEFAULT_CORPUS_SIZE):
        self.words = list(self.get_words(news_list or [], size))

    @classmethod
    def from_user(cls, user,
                  nsize=DEFAULT_NEWS_SIZE, 
                  csize=DEFAULT_CORPUS_SIZE):
        news_list = [n for s in user.schedules for n in s.news_list][:nsize]
        return cls(news_list, csize)

    @classmethod
    def from_random(cls, nsize=DEFAULT_NEWS_SIZE, csize=DEFAULT_CORPUS_SIZE):
        news_list = News.query.all()[:nsize]
        return cls(news_list, csize)

    @staticmethod
    def get_words(news_list, size):
        words = (w for n in news_list for w in n.words)
        counts = Counter(words)
        return (w for w, c in counts.most_common(size))

    def extract_features(self, news):
        owner = news.schedule.owner
        counts = Counter(news.words)
        return [counts.get(w, 0) for w in self.words]

    @property
    def size(self):
        return len(self.words)
