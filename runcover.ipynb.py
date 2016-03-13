# coding: utf-8
from app import (
    create_celery,
    create_news_backend,
    create_news_scheduler
)
from news.cover import Cover

celery = create_celery(app)
backend = create_news_backend(app)
scheduler = create_news_scheduler(backend, celery)
schedule = backend.get_schedules()[0]
scheduler.run.delay(schedule.id)
