from __future__ import absolute_import
import time
from celery import Celery
from redis import Redis, ConnectionPool
from flask import session
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import (
    LoginManager,
    current_user,
    encode_cookie,
)
from flask.ext.marshmallow import Marshmallow
from flask.ext.mail import Mail
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from news.utils.logging import logger
from news.backends.sqlalchemy import SQLAlchemyBackend
from news.persister import Persister
from news.scheduler import Scheduler
from autobahn.asyncio.wamp import ApplicationSession
from asyncio import coroutine
from .constants import (
    REDIS_COVER_FINISHED_CHANNEL,
    REDIS_COVER_START_CHANNEL,
    TOPIC_COVER_STARTED,
    TOPIC_COVER_FINISHED,
)


# ==========
# Extensions
# ==========

# redis instance
redis = Redis()

# celery instance
celery = Celery()

# scheduler
scheduler = Scheduler()

# schedule persister
persister = Persister(redis)

# app db instance
db = SQLAlchemy()

# marshmallow instance
ma = Marshmallow()

# app login manager instance
login_manager = LoginManager()

# app mail extension instance
mail = Mail()

# admin instance
admin = Admin()


# notifier component
class NotifierComponent(ApplicationSession):
    def notify(self, topic, message):
        logger.info(
            '[Notifier] push {} on {} to the router'
            .format(message, topic)
        )
        self.publish(topic, message)

    @coroutine
    def onJoin(self, details):
        self.pubsub = redis.pubsub()
        self.pubsub.subscribe(**{
            # publish notification to crossbar router on cover start
            REDIS_COVER_START_CHANNEL: lambda message:
            self.notify(TOPIC_COVER_STARTED, int(message['data'])),

            # publish notification to crossbar router on cover finish
            REDIS_COVER_FINISHED_CHANNEL: lambda message:
            self.notify(TOPIC_COVER_FINISHED, int(message['data']))
        })
        while True:
            self.pubsub.get_message()
            time.sleep(0.1)

# notifier component alias
notifier = NotifierComponent


# =============
# Configuration
# =============

def configure_redis(app):
    connection_pool = ConnectionPool(
        host=app.config.get('REDIS_HOST', 'localhost'),
        port=app.config.get('REDIS_PORT', 6379),
        db=app.config.get('REDIS_DB', 0),
    )
    redis.connection_pool = connection_pool


def configure_persister(app):
    persister.context = app.app_context()


def configure_celery(app):
    TaskBase = celery.Task

    # wrap celery task in flask app context
    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    # monkey patch celery task and configurations
    celery.Task = ContextTask
    celery.conf.update(app.config)


def configure_scheduler(app, user_model, schedule_model, news_model):
    # bind models with app config and create scheduler backend
    backend = SQLAlchemyBackend(
        owner_model=user_model,
        schedule_model=schedule_model,
        news_model=news_model,
        bind=db.session
    )

    # push notification on cover start and finish
    def on_cover_start(schedule):
        redis.publish(REDIS_COVER_START_CHANNEL, str(schedule.id))

    def on_cover_finish(schedule, news_list):
        redis.publish(REDIS_COVER_FINISHED_CHANNEL, str(schedule.id))

    scheduler.configure(backend=backend, celery=celery, persister=persister)


def configure_db(app):
    db.init_app(app)


def configure_ma(app):
    ma.init_app(app)


def configure_login(app):
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'
    login_manager.login_message = 'Please log in to Anchor to enter this page!'

    from .users.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)


def configure_mail(app):
    mail.init_app(app)


def configure_admin(app):
    user_model_view = type(
        'UserModelView', (ModelView,),
        {'form_excluded_columns': ['password_hash']}
    )
    schedule_model_view = type('ScheduleModelView', (ModelView,), {})
    news_model_view = type('NewsModelView', (ModelView,), {})
    rating_model_view = type('RatingModelView', (ModelView,), {})

    from .users.models import User
    from .schedules.models import Schedule
    from .news.models import News, Rating

    admin.init_app(app)
    admin.add_views(
        user_model_view(User, db.session),
        schedule_model_view(Schedule, db.session),
        news_model_view(News, db.session),
        rating_model_view(Rating, db.session),
    )


def register_blueprints(app, *blueprints):
    [app.register_blueprint(bp, url_prefix='/api') for bp in blueprints]
