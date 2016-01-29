#!/usr/bin/env python
from getpass import getpass

from flask.ext.script import Manager, Command
from flask.ext.migrate import Migrate, MigrateCommand

from config import Dev
from app import (
    create_app,
    setup_db
)
from app.users.models import User
from app.extensions import db


app = create_app(Dev)
manager = Manager(app)
migrate = Migrate(app, db)

class CreateSuperUser(Command):
    def run(self):
        email = raw_input('Enter user email: ')
        firstname = raw_input('Enter user\'s firstname: ')
        lastname = raw_input('Enter user\'s last name: ')
        password = getpass('Enter user\'s password: ')
        password_check = getpass('Enter user\'s password again: ')

        assert(password == password_check)

        with app.app_context():
            user = User(firstname, lastname, email, password)
            db.session.add(user)
            db.session.commit()

manager.add_command('db', MigrateCommand)
manager.add_command('createsuperuser', CreateSuperUser)


if __name__ == "__main__":
    manager.run()
