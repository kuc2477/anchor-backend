from wtforms import (
    Form,
    StringField,
    IntegerField,
    FieldList,
)
from wtforms.validators import (
    URL,
    NumberRange,
    Length
)
from ..utils.form import abort_on_validation_fail


class BaseScheduleForm(Form):
    name = StringField('Name', [Length(min=2, max=50)])
    url = StringField('Url', [URL()])
    cycle = IntegerField('Cycle', [NumberRange(min=5, max=600)])
    max_depth = IntegerField('Max depth', [NumberRange(max=5)])
    max_dist = IntegerField('Max distance', [NumberRange(max=5)])
    brothers = FieldList(StringField('Brother', [URL()]))
    blacklist = FieldList(StringField('Blacklist', [Length(min=2, max=10)]))


@abort_on_validation_fail
class ScheduleCreateForm(BaseScheduleForm):
    owner = IntegerField('Owner', [NumberRange(min=0)])


@abort_on_validation_fail
class ScheduleUpdateForm(BaseScheduleForm):
    id = IntegerField('Schedule ID')
