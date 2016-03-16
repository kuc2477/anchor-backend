from __future__ import print_function
from __future__ import absolute_import
from getpass import getpass

from flask.ext.script import Manager, Command
from flask.ext.migrate import Migrate, MigrateCommand

from config import Dev
from app import (
    create_app,
    create_celery,
    create_news_backend,
    create_news_scheduler
)
from app.users.models import User
from app.extensions import db


app = create_app(Dev)
celery = create_celery(app)
news_backend = create_news_backend(app)
news_scheduler = create_news_scheduler(news_backend, celery)

manager = Manager(app)
migrate = Migrate(app, db)


class CreateSuperUser(Command):
    def run(self):
        email = input('Enter user email: ')
        firstname = input('Enter user\'s firstname: ')
        lastname = input('Enter user\'s last name: ')
        password = getpass('Enter user\'s password: ')
        password_check = getpass('Enter user\'s password again: ')

        assert(password == password_check)

        with app.app_context():
            user = User(firstname, lastname, email, password)
            db.session.add(user)
            db.session.commit()


class RunCeleryServer(Command):
    def run(self):
        with app.app_context():
            celery.worker_main(['worker'])


class RunNewsScheduler(Command):
    def run(self):
        with app.app_context():
            news_scheduler.start()


manager.add_command('db', MigrateCommand)
manager.add_command('createsuperuser', CreateSuperUser)
manager.add_command('runcelery', RunCeleryServer)
manager.add_command('runscheduler', RunNewsScheduler)


if __name__ == "__main__":
    manager.run()
