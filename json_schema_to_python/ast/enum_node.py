import ast

from json_schema_to_python import json_schema
from json_schema_to_python.ast.literal_node import create_literal_node
from .types import AstName


def create_enum_node(
    schema: json_schema.types.EnumableSchema,
) -> ast.Assign:
    assert schema.enum is not None

    # return create_literal_node(schema)

    # This seems OK to hardcode as 0 for all attributes
    lineno = 0

    return ast.Assign(
        lineno=lineno,
        targets=[ast.Name(id=schema.get_schema_name())],
        value=create_literal_node(schema),
    )

    body = [
        ast.Assign(
            lineno=lineno,
            targets=[ast.Name(id=member)],
            value=ast.Constant(value=member),
        )
        for member in schema.enum
    ]

    return ast.ClassDef(
        bases=[AstName.Enum],
        body=body,
        decorator_list=[],
        keywords=[],
        name=schema.get_schema_name(),
    )
