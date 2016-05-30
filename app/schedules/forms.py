from wtforms import (
    Form,
    StringField,
    IntegerField,
    BooleanField,
    FieldList,
    FormField,
)
from wtforms.validators import (
    URL,
    NumberRange,
    Length,
    Optional
)
from ..utils.form import abort_on_validation_fail


class ScheduleOptionForm(Form):
    max_dist = IntegerField('Maximum Reporter Visit Distance', [
        Optional(), NumberRange(max=5)
    ])
    max_visit = IntegerField('Maximum Reporter Visit', [
        Optional(), NumberRange(max=200)
    ])
    url_whitelist = FieldList(StringField('URL Whitelist', [
        Optional(), URL()
    ]))
    url_blacklist = FieldList(StringField('URL Blacklist'), [
        Optional(), URL()
    ])
    ext_blacklist = FieldList(StringField('File Extension Blacklist'), [
        Optional()
    ])


class BaseScheduleForm(Form):
    name = StringField('Name', [Length(min=2, max=50)])
    url = StringField('Url', [URL()])
    type = StringField('News Type')
    cycle = IntegerField('Cycle', [Optional(), NumberRange(max=600)])
    enabled = BooleanField('Enabled', [Optional()])
    options = FormField(ScheduleOptionForm, [Optional()])


@abort_on_validation_fail
class ScheduleCreateForm(BaseScheduleForm):
    owner = IntegerField('Owner', [NumberRange(min=0), Optional()])


@abort_on_validation_fail
class ScheduleUpdateForm(BaseScheduleForm):
    id = IntegerField('Schedule ID')
