from flask import Blueprint
from flask.ext.restful import Api
from .models import (
    NewsResource,
    NewsListResource,
    RatingResource,
    RatingListResource,
)


# news blueprint
bp = Blueprint('news_bp', __name__, template_folder='templates')
api = Api(bp)
api.add_resource(NewsResource, '/news/<int:id>')
api.add_resource(NewsListResource, '/news')
api.add_resource(RatingResource, '/ratings/<int:id>')
api.add_resource(RatingListResource, '/ratings')
