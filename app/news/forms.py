from wtforms import (
    Form,
    IntegerField,
    BooleanField,
)
from wtforms.validators import Optional
from ..utils.form import abort_on_validation_fail


@abort_on_validation_fail
class BaseRatingForm(Form):
    positive = BooleanField('Positive')


@abort_on_validation_fail
class RatingDetailForm(BaseRatingForm):
    user = IntegerField('User', [Optional()])
    news = IntegerField('News')
