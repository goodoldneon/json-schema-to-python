import ast

from json_schema_to_model import json_schema
from json_schema_to_model.json_schema.utils import convert_schema_id_to_name
from .types import AstName, convert_json_schema_type_to_ast_name


def create_union_node(
    schemas: list[json_schema.types.Schema],
) -> ast.Subscript:
    """
    Create a `Union` AST node
    """

    dims: list[ast.Name] = []
    for schema in schemas:
        if isinstance(schema, json_schema.types.AllOfSchema):
            raise NotImplementedError()
        elif isinstance(schema, json_schema.types.AnyOfSchema):
            raise NotImplementedError()
        elif isinstance(schema, json_schema.types.Ref):
            dims.append(ast.Name(id=convert_schema_id_to_name(schema.ref)))
        else:
            dims.append(convert_json_schema_type_to_ast_name(schema.type))

    return ast.Subscript(
        slice=ast.Tuple(dims=dims),
        value=AstName.Union,
    )
