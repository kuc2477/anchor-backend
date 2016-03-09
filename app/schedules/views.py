from flask import Blueprint
from flask.ext.restful import Api


# schedules bluepring
schedules = Blueprint('schedules', __name__, template_folder='templates')
schedules_api = Api(schedules)
