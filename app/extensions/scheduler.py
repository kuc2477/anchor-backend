from news.scheduler import Scheduler
from news.backends.sqlalchemy import SQLAlchemyBackend
from news.contrib.logging.middlewares import (
    request_log_middleware,
    response_log_middleware,
    report_log_middleware,
)
from .app import db
from .celery import celery
from .redis import redis
from .persister import persister
from ..constants import (
    REDIS_COVER_START_CHANNEL,
    REDIS_COVER_SUCCESS_CHANNEL,
    REDIS_COVER_ERROR_CHANNEL,
)


scheduler = Scheduler()


def configure_scheduler(app, user_model, schedule_model, news_model):
    # bind models with app config and create scheduler backend
    backend = SQLAlchemyBackend(
        owner_model=user_model,
        schedule_model=schedule_model,
        news_model=news_model,
        bind=db.session
    )

    # middlwares
    request_middlewares = [request_log_middleware]
    response_middlewares = [response_log_middleware]
    report_middlewares = [report_log_middleware]

    # callbacks
    def on_cover_start(schedule):
        redis.publish(REDIS_COVER_START_CHANNEL, str(schedule.id))

    def on_cover_success(schedule, news_list):
        redis.publish(REDIS_COVER_SUCCESS_CHANNEL, str(schedule.id))

    def on_cover_error(schedule, exc):
        redis.publish(REDIS_COVER_ERROR_CHANNEL, str(schedule.id))

    scheduler.configure(
        backend=backend, celery=celery, persister=persister,
        request_middlewares=request_middlewares,
        response_middlewares=response_middlewares,
        report_middlewares=report_middlewares,
        on_cover_start=on_cover_start,
        on_cover_success=on_cover_success,
        on_cover_error=on_cover_error,
    )
