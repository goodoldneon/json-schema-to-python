import ast

from json_schema_to_model import json_schema
from .types import AstName


def create_literal_node(
    schema: json_schema.types.EnumableSchema,
) -> ast.Subscript:
    """
    Create a `Literal` AST node
    """

    assert schema.enum is not None

    dims: list[ast.Constant] = []
    for member in schema.enum:
        dims.append(ast.Constant(value=member))

    return ast.Subscript(
        slice=ast.Tuple(dims=dims),
        value=AstName.Literal,
    )
