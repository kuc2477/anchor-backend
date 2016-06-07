from app.extensions import scheduler, db
from app.users.models import User
from app.schedules.models import Schedule
from news.cover import Cover
from news.reporters.url import URLReporter
from news.reporters.feed import AtomReporter, RSSReporter
from news.contrib.logging.middlewares import (
    logging_dispatch_middleware,
    logging_fetch_middleware,
)


schedule = Schedule.query.first()
backend = scheduler.backend
cover = Cover(schedule, backend)
cover.prepare(
    reporter_class=URLReporter,
    dispatch_middlewares=[logging_dispatch_middleware],
    fetch_middlewares=[logging_fetch_middleware],
)
