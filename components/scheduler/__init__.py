from news.backends.sqlalchemy import SQLAlchemyBackend
from news.scheduler import Scheduler

from ..server.users.models import User
from ..server.schedules.models import Schedule
from ..server.news.models import News
from ..server.extensions import db, persister


def create_news_backend(app):
    return SQLAlchemyBackend(
        bind=db.session,
        owner_class=User,
        schedule_class=Schedule,
        news_class=News
    )


def create_news_scheduler(backend, celery):
    return Scheduler(backend, celery, persister=persister)
