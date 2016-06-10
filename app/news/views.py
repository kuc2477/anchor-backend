from flask import (
    Blueprint,
    request,
    jsonify
)
from flask.ext.login import current_user
from flask.ext.restful import Api
from flask.ext.restful import abort
from ..extensions import db
from .models import News, Rating
from .resources import (
    NewsResource,
    NewsListResource,
    LatestListResource,
    RecommListResource,
)
from .forms import BaseRatingForm


# news blueprint
bp = Blueprint('news_bp', __name__, template_folder='templates')
api = Api(bp)
api.add_resource(NewsResource, '/news/<int:id>')
api.add_resource(NewsListResource, '/news')
api.add_resource(LatestListResource, '/news/latest')
api.add_resource(RecommListResource, '/news/recomms')


@bp.route('/news/<int:id>/ratings', methods=['POST', 'PUT'])
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
        or Rating(user=user, news=news, positive=positive)

    # save the rating and return serialized updated news
    if not rating.id:
        db.session.add(rating)
    else:
        rating.positive = positive

    db.session.commit()
    return jsonify(news.serialized), 200


@bp.route('/news/<int:id>/ratings', methods=['DELETE'])
def cancel_rating(id):
    if current_user.is_anonymous:
        abort(400)

    # check if news exists
    news = News.query.get_or_404(id)

    # find existing rating of the current user of target news
    rating = Rating.query.filter_by(
        news_id=id, user_id=current_user.id).first()

    # try to delete the existing rating
    if not rating:
        abort(404)
    else:
        db.session.delete(rating)
        db.session.commit()

    return jsonify(news.serialized), 204
