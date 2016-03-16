from marshmallow import fields
from marshmallow_sqlalchemy.convert import ModelConverter
from sqlalchemy_utils.types import JSONType
from ..extensions import ma


class JSONTypeCoverter(ModelConverter):
    SQLA_TYPE_MAPPING = dict(
        list(ModelConverter.SQLA_TYPE_MAPPING.items()) +
        [(JSONType, (lambda *args, **kwargs:
                     lambda *field_args, **field_kwargs:
                     fields.List(fields.Str)))]
    )


def get_base_schema(m):
    class Schema(ma.ModelSchema):
        class Meta:
            model = m
            model_converter = JSONTypeCoverter
    return Schema
