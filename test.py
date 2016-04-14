from app import create_app, create_scheduler_backend
from app.schedules.models import Schedule
from news.cover import Cover
from config import Dev

app = create_app(Dev)
with app.app_context():
    backend = create_scheduler_backend(app)
    schedule = Schedule.query.first()
    cover = Cover.from_schedule(schedule, backend)
    cover.run()
