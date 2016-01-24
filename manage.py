#!/usr/bin/env python
from flask.ext.script import Manager

from config import Dev
from app import (
    create_app,
    setup_db
)


app = create_app(Dev)
manager = Manager(app)


@manager.option('-c', '--config', default='dev', type=str,
                choices=['dev', 'test', 'prod'])
def run(config):
    create_app(config.title()).run(debug=True)



if __name__ == "__main__":
    manager.run()
