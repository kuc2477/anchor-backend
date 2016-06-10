from news.persister import Persister
from .redis import redis

persister = Persister(redis)


def configure_persister(app):
    persister.context = app.app_context()
