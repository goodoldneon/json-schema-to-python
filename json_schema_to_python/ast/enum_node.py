import ast

from json_schema_to_python import json_schema
from json_schema_to_python.ast.literal_node import create_literal_node


def create_enum_node(
    schema: json_schema.types.EnumableSchema,
) -> ast.Assign:
    assert schema.enum is not None

    # This seems OK to hardcode as 0 for all attributes
    lineno = 0

    return ast.Assign(
        lineno=lineno,
        targets=[ast.Name(id=schema.get_schema_name())],
        value=create_literal_node(schema),
    )
