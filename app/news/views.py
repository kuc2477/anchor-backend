from flask import Blueprint
from flask import request
from flask.ext.login import current_user
from flask.ext.restful import Api
from flask.ext.restful import abort
from ..extensions import db
from .models import (
    News,
    Rating,
    NewsResource,
    NewsListResource,
)
from .forms import (
    BaseRatingForm,
    RatingDetailForm
)


# news blueprint
bp = Blueprint('news_bp', __name__, template_folder='templates')
api = Api(bp)
api.add_resource(NewsResource, '/news/<int:id>')
api.add_resource(NewsListResource, '/news')


@bp.route('/api/news/<int:id>/ratings', methods=['POST', 'PUT'])
def rate_news(id):
    form = BaseRatingForm(**request.json)
    form.validate()

    if current_user.is_anonymous:
        abort(400)

    # post data
    news = News.query.get_or_404(id)
    user = current_user
    positive = form.positive.data

    # find existing rating or create new one otherwise
    rating = Rating.query.filter_by(news_id=news.id, user_id=user.id).first() \
        or Rating(user=user, news=news.id, positive=positive)

    # save the rating and return serialized updated news
    if not rating.id:
        db.session.add(rating)
    else:
        rating.positive = positive

    db.session.commit()
    return news.serialized, 200


@bp.route('/api/news/<int:id>/ratings', methods=['DELETE'])
def cancel_rating(id):
    form = RatingDetailForm(**request.json)
    form.validate()

    if current_user.is_anonymous:
        abort(400)

    # post data
    news = News.query.get_or_404(id)
    user_id = form.user.data or current_user.id

    # find existing rating of the current user of target news
    rating = Rating.query.filter_by(news_id=news.id, user_id=user_id).first()

    # try to delete the existing rating
    if not rating:
        abort(404)
    else:
        db.session.delete(rating)
        db.session.commit()

    return news.serialized, 204
