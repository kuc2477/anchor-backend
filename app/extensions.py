from celery import Celery
from redis import Redis, ConnectionPool
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.marshmallow import Marshmallow
from flask.ext.mail import Mail
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from news.backends.sqlalchemy import SQLAlchemyBackend
from news.persister import Persister
from news.scheduler import Scheduler


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
