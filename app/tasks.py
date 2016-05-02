from flask import current_app
from .extensions import celery, scheduler


# create app to make sure all app extensions are configured properly
if not current_app:
    from app import create_app_from_env
    create_app_from_env()


# run news reporting cover
run_cover = scheduler.make_task()


# run learning
@celery.task
def fit_svm(classifier_id):
    from .news.models import News
    from .classifiers.models import SVM
    svm = SVM.query.get(classifier_id)
    training_set = News.query.filter(News.user_id == svm.user.id).all()
    svm.fit(training_set)

@celery.task
def fit_svm_for(user_id):
    from .news.models import News
    from .users.models import User
    user = User.query.get(user_id)
    # TODO: NOT IMPLEMENTED YET
