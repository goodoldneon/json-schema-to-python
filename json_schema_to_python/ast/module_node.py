import ast
from json_schema_to_python.json_schema.types import (
    ObjectSchema,
    Schema,
    is_enumable_schema,
)
from .class_node import create_class_node
from .enum_node import create_enum_node
from .import_node import create_import_nodes


def create_module_node(model_schemas: list[Schema]) -> ast.Module:
    class_nodes = [
        create_class_node(schema)
        for schema in model_schemas
        if isinstance(schema, ObjectSchema)
    ]

    enum_nodes = [
        create_enum_node(schema)
        for schema in model_schemas
        if is_enumable_schema(schema)
    ]

    return ast.Module(
        body=[
            *create_import_nodes(),
            *class_nodes,
            *enum_nodes,
        ],
        type_ignores=[],
    )
