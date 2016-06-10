from __future__ import absolute_import
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.marshmallow import Marshmallow
from flask.ext.mail import Mail
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView


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


def configure_db(app):
    db.init_app(app)


def configure_ma(app):
    ma.init_app(app)


def configure_login(app):
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'
    login_manager.login_message = 'Please log in to Anchor to enter this page!'

    from ..users.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)


def configure_mail(app):
    mail.init_app(app)


def configure_admin(app):
    from ..users.models import User
    from ..schedules.models import Schedule
    from ..news.models import News, Rating
    from ..corpuses.models import Corpus
    from ..clsfiers.models import SVM

    admin.init_app(app)
    admin.add_views(
        ModelView(User, db.session),
        ModelView(Schedule, db.session),
        ModelView(News, db.session),
        ModelView(Rating, db.session),
        ModelView(Corpus, db.session),
        ModelView(SVM, db.session),
    )


def register_blueprints(app, *blueprints):
    [app.register_blueprint(bp, url_prefix='/api') for bp in blueprints]
