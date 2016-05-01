from datetime import datetime
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import (
    relationship, 
    backref
)
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime
)
from ..corpus.models import Corpus
from ..users.models import User
from ..extensions import db


class MLP(db.Model):
    @declared_attr
    def corpus_id(self):
        return Column(Integer, ForeignKey(Corpus.id))

    @declared_attr
    def corpus(self):
        return relationship(Corpus, backref='mlps')

    @declared_attr
    def user_id(cls):
        return Column(Integer, ForeignKey(User.id))

    @declared_attr
    def user(cls):
        return relationship(User, backref='mlps')

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def predict(self, news):
        features = self.corpus.extract_features(news)

    @classmethod
    def predict_for(self, user, news):
        pass
