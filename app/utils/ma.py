from marshmallow import fields
from marshmallow_sqlalchemy.convert import ModelConverter
from sqlalchemy_utils.types import JSONType


class JSONTypeCoverter(ModelConverter):
    SQLA_TYPE_MAPPING = dict(
        list(ModelConverter.SQLA_TYPE_MAPPING.items()) +
        [(JSONType, fields.Str)]
    )
