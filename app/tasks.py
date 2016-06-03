from flask import current_app
from .users.models import User
from .news.models import News
from .schedules.models import Schedule
from .clsfiers.models import SVM
from .extensions import celery, scheduler, db


# create app to make sure all app extensions are configured properly
if not current_app:
    from app import create_app_from_env
    create_app_from_env()


# =====
# Tasks
# =====

# run news reporting cover
run_cover = scheduler.make_task()


# run model fits
@celery.task
def fit_svm(id):
    svm = SVM.query.get(id)
    training_set = News.query.join(Schedule)\
        .filter(Schedule.owner_id == svm.user.id)\
        .all()
    svm.fit(training_set)
    db.session.commit()


@celery.task
def fit_svm_for(user_id):
    training_set = News.query.join(Schedule)\
        .filter(Schedule.owner_id == user_id)\
        .all()
    user = User.query.get(user_id)
    user.svm.fit(training_set)
    db.session.commit()
