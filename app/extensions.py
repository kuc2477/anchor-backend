from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask_admin import Admin


# ===================
# Extension instances
# ===================

# app db instance
db = SQLAlchemy()

# app login manager instance
login_manager = LoginManager()

# admin instance
admin = Admin()


# =============
# Setup methods
# =============

def configure_db(app):
    db.init_app(app)


def configure_login_manger(app):
    login_manager.init_app(app)

    from .users.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

def configure_admin(app):
    admin.init_app(app)
