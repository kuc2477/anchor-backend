from wtforms import (
    Form,
    StringField,
    IntegerField,
    BooleanField,
    FieldList,
)
from wtforms.validators import (
    URL,
    NumberRange,
    Length,
    Optional
)
from ..utils.form import abort_on_validation_fail


class BaseScheduleForm(Form):
    name = StringField('Name', [Length(min=2, max=50)])
    url = StringField('Url', [URL()])
    cycle = IntegerField('Cycle', [Optional(), NumberRange(max=600)])
    enabled = BooleanField('Enabled', [Optional()])
    max_depth = IntegerField('Max depth', [Optional(), NumberRange(max=5)])
    max_dist = IntegerField('Max distance', [Optional(), NumberRange(max=5)])
    brothers = FieldList(
        StringField('Brother', [Optional(), URL()])
    )
    blacklist = FieldList(
        StringField('Blacklist', [Optional(), Length(max=10)])
    )


@abort_on_validation_fail
class ScheduleCreateForm(BaseScheduleForm):
    owner = IntegerField('Owner', [NumberRange(min=0)])


@abort_on_validation_fail
class ScheduleUpdateForm(BaseScheduleForm):
    id = IntegerField('Schedule ID')
