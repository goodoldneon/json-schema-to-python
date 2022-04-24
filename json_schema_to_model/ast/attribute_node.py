import ast

from json_schema_to_model import json_schema
from json_schema_to_model.json_schema.types import Schema
from .list_node import create_list
from .literal_node import create_literal_node
from .types import AstName, convert_json_schema_type_to_ast_name
from .union_node import create_union_node


def get_attribute_node(
    property_name: str,
    property_schema: Schema,
    is_required: bool,
) -> ast.AnnAssign:
    type_value = _get_type_value(property_schema)

    annotation: ast.Name | ast.Subscript
    if is_required:
        annotation = type_value
    else:
        annotation = ast.Subscript(
            slice=type_value,
            value=AstName.NotRequired,
        )

    return ast.AnnAssign(
        annotation=annotation,
        simple=1,
        target=ast.Name(id=property_name),
    )


def _get_type_value(
    schema: json_schema.types.Schema,
) -> ast.Name | ast.Subscript:
    type_value: ast.Name | ast.Subscript

    if isinstance(schema, json_schema.types.ArraySchema):
        type_value = create_list(schema)
    elif isinstance(schema, json_schema.types.AllOfSchema):
        raise NotImplementedError()
    elif isinstance(schema, json_schema.types.AnyOfSchema):
        type_value = create_union_node(schema.anyOf.__root__)
    elif isinstance(schema, json_schema.types.MultiTypeSchema):
        type_value = create_union_node(schema.type)
    elif isinstance(schema, json_schema.types.Ref):
        type_value = ast.Name(id=schema.get_schema_name())
    else:
        if json_schema.types.is_enumable_schema(schema):
            type_value = create_literal_node(schema)
        else:
            type_value = convert_json_schema_type_to_ast_name(schema.type)

    return type_value
