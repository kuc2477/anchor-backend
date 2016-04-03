from __future__ import print_function
from __future__ import absolute_import
import os
import subprocess
import shutil
from getpass import getpass
from flask.ext.script import Manager, Command
from flask.ext.migrate import Migrate, MigrateCommand

import config
from app import (
    create_app,
    create_scheduler
)
from app.users.models import User
from app.extensions import (
    db, celery
)


try:
    config_name = os.environ['ANCHOR_CONFIG'].title()
except KeyError:
    config_name = 'Dev'


app = create_app(getattr(config, config_name))
scheduler = create_scheduler(app)

manager = Manager(app)
migrate = Migrate(app, db)


# ========
# Commands
# ========

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


class RunCelery(Command):
    def run(self):
        with app.app_context():
            celery.worker_main(['worker'])


class RunScheduler(Command):
    def run(self):
        with app.app_context():
            scheduler.start()


class RunRedis(Command):
    def run(self):
        subprocess.call(['redis-server'])


class RunBroker(Command):
    def run(self):
        if 'nt' in os.name:
            subprocess.call([shutil.which('rabbitmq-server'), 'start'])
        else:
            subprocess.call(['sudo', shutil.which('rabbitmq-server'), 'start'])


# Register commands
manager.add_command('db', MigrateCommand)
manager.add_command('createsuperuser', CreateSuperUser)
manager.add_command('runscheduler', RunScheduler)
manager.add_command('runcelery', RunCelery)
manager.add_command('runbroker', RunBroker)
manager.add_command('runredis', RunRedis)


if __name__ == "__main__":
    manager.run()
