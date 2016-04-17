from flask import current_app
from .extensions import celery, scheduler


# create app to make sure all app extensions are configured properly
if not current_app:
    from app import create_app_from_env
    create_app_from_env()


run_cover = scheduler.make_task()
