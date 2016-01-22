from flask.ext.sqlalchemy import SQLAlchemy

from . import create_app


db = SQLAlchemy()

# initialize database
def init_db(cfg):
    from .users import models as user_models
    from .sites import models as site_models
    from .pages import models as page_models
    from .schedules import models as schedule_models

    app = create_app(cfg)
    db.init_app(app)

    with app.app_context():
        db.create_all()
