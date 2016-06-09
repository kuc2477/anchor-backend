from app.extensions import scheduler, db
from app.users.models import User
from app.schedules.models import Schedule
from news.cover import Cover
from news.reporters.url import URLReporter
from news.reporters.feed import AtomReporter, RSSReporter
from news.contrib.logging.middlewares import (
    request_log_middleware,
    response_log_middleware,
    report_log_middleware,
)


schedule = Schedule.query.first()
backend = scheduler.backend
cover = Cover(schedule, backend)
cover.prepare(
    reporter_class=URLReporter,
    request_middlewares=[request_log_middleware],
    response_middlewares=[response_log_middleware],
    report_middlewares=[report_log_middleware],
)
