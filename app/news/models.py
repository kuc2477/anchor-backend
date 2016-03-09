from news.models.sqlalchemy import (
    create_abc_news, create_news
)

from ..schedules.models import Schedule
from ..extensions import db


News = create_news(create_abc_news(Schedule), db.Model)
