import pickle
import numpy as np
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
    corpus_backref_name = None
    user_backref_name = None

    @declared_attr
    def corpus_id(cls):
        return Column(Integer, ForeignKey(Corpus.id))

    @declared_attr
    def corpus(cls):
        return relationship(Corpus, backref=backref(
            cls.corpus_backref_name,
            cascade='delete, delete-orphan'
        ))

    @declared_attr
    def user_id(cls):
        return Column(Integer, ForeignKey(User.id), unique=True)

    @declared_attr
    def user(cls):
        return relationship(User, backref=backref(
            cls.user_backref_name, uselist=False,
            cascade='delete, delete-orphan'
        ))

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

    def label(self, rating):
        if rating is None:
            return 0
        elif rating:
            return 1
        else:
            return -1

    def delabel(self, label):
        if label == 0:
            return None
        elif label > 0:
            return True
        else:
            return False

    def fit(self, training_set):
        X = [self.corpus.extract_features(n) for n in training_set]
        y = [self.label(n.get_rating(self.user)) for n in training_set]

        model = self.model or self.model_class()
        model.fit(X, y)
        self.model = model
        return self.model

    def predict(self, news):
        return self.predict_bulk([news])

    def predict_bulk(self, news_list):
        if not self.model:
            return None
        X = np.array([self.corpus.extract_features(n) for n in news_list])
        return [self.delabel(y) for y in self.model.predict(X)]


class SVM(AbstractClassifier, db.Model):
    model_class = SVC
    user_backref_name = 'svm'
    corpus_backref_name = 'svms'
