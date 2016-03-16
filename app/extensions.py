from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.marshmallow import Marshmallow
from flask.ext.mail import Mail
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView


# ===================
# Extension instances
# ===================

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
# Setup methods
# =============

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

    from .users.models import User
    from .schedules.models import Schedule
    from .news.models import News

    admin.init_app(app)
    admin.add_views(
        user_model_view(User, db.session),
        schedule_model_view(Schedule, db.session),
        news_model_view(News, db.session)
    )


def register_blueprints(app, *blueprints):
    [app.register_blueprint(bp) for bp in blueprints]
