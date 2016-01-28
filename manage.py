#!/usr/bin/env python
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from config import Dev
from app import (
    create_app,
    setup_db
)
from app.extensions import db


app = create_app(Dev)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    manager.run()
