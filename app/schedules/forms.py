from wtforms import (
    Form, TextField
)
from wtforms.validators import (
    Email,
    Length,
    EqualTo,
)
from ..utils.form import abort_on_validation_fail


@abort_on_validation_fail
class ScheduleCreateForm(Form):
    # TODO: NOT IMPLEMENTED YET
    pass


@abort_on_validation_fail
class ScheduleUpdateForm(Form):
    # TODO: NOT IMPLEMENTED YET
    pass


@abort_on_validation_fail
class ScheduleDeleteForm(Form):
    # TODO: NOT IMPLEMENTED YET
    pass
