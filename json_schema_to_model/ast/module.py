import ast
from json_schema_to_model.json_schema.types import ObjectSchema, Schema
from .class_def import create_class_def
from .imports import create_imports


def create_module(model_schemas: list[Schema]) -> ast.Module:
    model_defs = [
        create_class_def(schema)
        for schema in model_schemas
        if isinstance(schema, ObjectSchema)
    ]

    return ast.Module(
        body=[
            *create_imports(),
            *model_defs,
        ],
        type_ignores=[],
    )
