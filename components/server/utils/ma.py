from marshmallow import fields
from marshmallow_sqlalchemy.convert import ModelConverter
from sqlalchemy_utils.types import JSONType
from ..extensions import ma


def use_json_type_as_array(model_converter):
    converter_factory = \
        lambda *args, **kwargs: \
        lambda *fargs, **fkwargs: fields.List(fields.Str)

    model_converter.SQLA_TYPE_MAPPING.update([(JSONType, converter_factory)])
    return model_converter


def get_base_schema(m):
    class Schema(ma.ModelSchema):
        class Meta:
            model = m
            model_converter = use_json_type_as_array(ModelConverter)
    return Schema
