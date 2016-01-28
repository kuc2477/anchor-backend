#!/usr/bin/env python
from flask.ext.script import Manager

from config import Dev
from app import (
    create_app,
    setup_db
)


app = create_app(Dev)
manager = Manager(app)


if __name__ == "__main__":
    manager.run()
