from flask import Blueprint
from flask.ext.restful import Api
from .models import (
    ScheduleResource,
    ScheduleListResource
)


# schedules blueprint
bp = Blueprint('schedules_bp', __name__, template_folder='templates')
api = Api(bp)
api.add_resource(ScheduleResource, '/schedules/<int:id>')
api.add_resource(ScheduleListResource, '/schedules')
