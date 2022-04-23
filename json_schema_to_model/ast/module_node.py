import ast
from json_schema_to_model.json_schema.types import ObjectSchema, Schema
from .class_node import create_class_node
from .import_node import create_import_nodes


def create_module_node(model_schemas: list[Schema]) -> ast.Module:
    class_nodes = [
        create_class_node(schema)
        for schema in model_schemas
        if isinstance(schema, ObjectSchema)
    ]

    return ast.Module(
        body=[
            *create_import_nodes(),
            *class_nodes,
        ],
        type_ignores=[],
    )
