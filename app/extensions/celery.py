from celery import Celery


celery = Celery()


def configure_celery(app):
    TaskBase = celery.Task

    # wrap celery task in flask app context
    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    # monkey patch celery task and configurations
    celery.Task = ContextTask
    celery.conf.update(app.config)
