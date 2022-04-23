import ast

from json_schema_to_model import json_schema
from json_schema_to_model.json_schema.utils import convert_schema_id_to_name
from .types import AstName, convert_json_schema_type_to_ast_name
from .union_node import create_union_node


def create_list(schema: json_schema.types.ArraySchema) -> ast.Subscript:
    """
    Create a `list` AST node
    """

    slice: ast.Name | ast.Subscript
    if len(schema.items) == 0:
        raise Exception("empty array items")
    if len(schema.items) == 1:
        subschema = schema.items[0]

        if isinstance(subschema, json_schema.types.AllOfSchema):
            raise NotImplementedError()
        elif isinstance(subschema, json_schema.types.AnyOfSchema):
            raise NotImplementedError()
        elif isinstance(subschema, json_schema.types.Ref):
            slice = ast.Name(id=convert_schema_id_to_name(subschema.ref))
        else:
            slice = convert_json_schema_type_to_ast_name(subschema.type)
    else:
        slice = create_union_node(schema.items)

    return ast.Subscript(
        slice=slice,
        value=AstName.list,
    )
