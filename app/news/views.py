from flask import Blueprint
from flask.ext.restful import Api
from .models import NewsResource


# news blueprint
bp = Blueprint('news_bp', __name__, template_folder='templates')
api = Api(bp)
api.add_resource(NewsResource)
