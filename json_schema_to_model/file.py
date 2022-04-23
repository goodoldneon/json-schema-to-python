import ast

from json_schema_to_model.ast import create_class_def, create_imports
from json_schema_to_model.json_schema.types import ObjectSchema, Schema


def convert_schemas_to_file_content(schemas: list[Schema]) -> str:
    class_defs = [
        create_class_def(schema) for schema in schemas
        if isinstance(schema, ObjectSchema)
    ]


    tree = ast.Module(
        body=[
            *create_imports(),
            *class_defs,
        ],
        type_ignores=[],
    )

    return ast.unparse(tree)
