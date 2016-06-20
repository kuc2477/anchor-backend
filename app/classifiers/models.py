import pickle
from datetime import datetime
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship, backref
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
    LargeBinary
)
from sklearn.feature_extraction import DictVectorizer
from sklearn.svm import SVC
from ..users.models import User
from ..corpuses.models import Corpus
from ..extensions import db


class AbstractClassifier(object):
    model_class = None
    corpus_backref_name = None
    user_backref_name = None
    vectorizer = DictVectorizer()

    @declared_attr
    def corpus_id(cls):
        return Column(Integer, ForeignKey(Corpus.id))

    @declared_attr
    def corpus(cls):
        return relationship(Corpus, backref=backref(
            cls.corpus_backref_name, lazy='dynamic',
            cascade='delete-orphan, all',
            cascade_backrefs=False,
        ))

    @declared_attr
    def user_id(cls):
        return Column(Integer, ForeignKey(User.id))

    @declared_attr
    def user(cls):
        return relationship(User, backref=backref(
            cls.user_backref_name, lazy='dynamic',
            cascade='delete-orphan, all',
            cascade_backrefs=False,
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

    def get_X(self, news_list):
        X_dicts = [self.corpus.extract_features(n) for n in news_list]
        return self.vectorizer.fit_transform(X_dicts).toarray()

    def get_y(self, news_list):
        return [str(n.get_rating(user=self.user)) for n in news_list]

    def deserialize_predictions(self, predictions):
        return [eval(p) for p in predictions]

    # =========================
    # Classifier Main Interface
    # =========================

    def fit(self, training_set):
        X = self.get_X(training_set)
        y = self.get_y(training_set)
        model = self.model or self.model_class()
        model.fit(X, y)
        self.model = model
        return self.model

    def predict(self, news_list):
        if not self.model:
            return None
        X = self.get_X(news_list)
        y = self.model.predict(X)
        return self.deserialize_predictions(y)


class SVM(AbstractClassifier, db.Model):
    model_class = SVC
    corpus_backref_name = 'svms'
    user_backref_name = 'svms'
