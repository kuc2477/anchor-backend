from marshmallow import fields
from marshmallow_sqlalchemy.convert import ModelConverter
from sqlalchemy_utils.types import JSONType


class JSONTypeCoverter(ModelConverter):
    SQLA_TYPE_MAPPING = dict(
        list(ModelConverter.SQLA_TYPE_MAPPING.items()) +
        [(JSONType, (lambda *args, **kwargs:
                     lambda *field_args, **field_kwargs:
                     fields.List(fields.Str)))]
    )
