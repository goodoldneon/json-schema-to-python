import ast

from json_schema_to_model import json_schema
from json_schema_to_model.json_schema.utils import convert_schema_id_to_name
from .types import AstName


def create_enum_class_def(
    schema: json_schema.types.EnumableSchema,
) -> ast.ClassDef:
    assert schema.enum is not None
    assert schema.id is not None

    name = convert_schema_id_to_name(schema.id)

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
        name=name,
    )
