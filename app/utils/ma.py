from marshmallow import fields
from marshmallow_sqlalchemy.convert import ModelConverter
from sqlalchemy_utils.types import JSONType
from ..extensions import ma


def use_json_type_as_dict(model_coverter):
    coverter_factory = \
        lambda *args, **kwargs: \
        lambda *fargs, **fkwargs: fields.Dict()

    model_coverter.SQLA_TYPE_MAPPING.update([(JSONType, coverter_factory)])
    return model_coverter


def use_json_type_as_array(model_converter):
    converter_factory = \
        lambda *args, **kwargs: \
        lambda *fargs, **fkwargs: fields.List(fields.Str)

    model_converter.SQLA_TYPE_MAPPING.update([(JSONType, converter_factory)])
    return model_converter


def get_base_schema(m, json_field='list'):
    class Schema(ma.ModelSchema):
        class Meta:
            model = m
            model_converter = \
                use_json_type_as_array(ModelConverter) if json_field == 'list'\
                else use_json_type_as_dict(ModelConverter)
    return Schema
