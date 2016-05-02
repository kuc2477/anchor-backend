import pickle
from datetime import datetime
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
    LargeBinary
)
from sklearn.svm import SVC
from ..corpus.models import Corpus
from ..users.models import User
from ..extensions import db


class AbstractClassifier(object):
    model_class = None

    @declared_attr
    def __table__args(cls):
        return (UniqueConstraint('corpus_id', 'user_id'),)

    @declared_attr
    def corpus_id(cls):
        return Column(Integer, ForeignKey(Corpus.id))

    @declared_attr
    def corpus(cls):
        return relationship(Corpus, backref=cls.__table_name__.lower())

    @declared_attr
    def user_id(cls):
        return Column(Integer, ForeignKey(User.id))

    @declared_attr
    def user(cls):
        return relationship(User, backref=backref(
            cls.__table_name__.lower(), uselist=False))

    def __init__(self, user, corpus):
        self.user = user
        self.corpus = corpus

    id = Column(Integer, primary_key=True)
    serialized = Column(LargeBinary, nullable=False)
    created = Column(DateTime, default=datetime.now)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    @property
    def model(self):
        if self.serialized is None:
            return None
        else:
            return pickle.loads(self.serialized)

    @model.setter
    def model(self, classifier):
        self.serialized = pickle.dumps(classifier)

    def fit(self, training_set):
        X = [self.corpus.extract_features(n) for n in training_set]
        y = [n.get_rating(self.user) for n in training_set]

        model = self.model or self.model_class()
        model.fit(X, y)
        self.model = model
        return self.model

    def predict(self, news):
        if not self.model:
            return None
        features = self.corpus.extract_features(news)
        return self.model.predict(features)


class SVM(AbstractClassifier, db.Model):
    model_class = SVC
