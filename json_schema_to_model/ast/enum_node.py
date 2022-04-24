import ast

from json_schema_to_model import json_schema
from .types import AstName


def create_enum_node(
    schema: json_schema.types.EnumableSchema,
) -> ast.ClassDef:
    assert schema.enum is not None

    # This seems OK to hardcode as 0 for all attributes
    lineno = 0

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
