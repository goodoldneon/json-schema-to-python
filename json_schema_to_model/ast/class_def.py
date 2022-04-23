import ast

from json_schema_to_model import json_schema
from json_schema_to_model.json_schema.types import Ref
from .types import AstName, convert_json_schema_type_to_ast_name

def convert_object_schema_to_class_def(
    schema: json_schema.types.ObjectSchema,
) -> ast.ClassDef:
    """
    Convert a schema object into an AST class definition
    """

    assert schema.id is not None
    name = schema.id.split("#")[-1]

    class_def = ast.ClassDef(
        bases=[AstName.TypedDict],
        body=[],
        decorator_list=[],
        keywords=[],
        name=name,
    )

    for k, v in schema.properties.items():
        type_value = _get_type_value(v)

        if k in schema.required:
            annotation: ast.Name | ast.Subscript = type_value
        else:
            annotation = ast.Subscript(
                slice=type_value,
                value=AstName.NotRequired,
            )

        prop_def = ast.AnnAssign(
            annotation=annotation,
            simple=1,
            target=ast.Name(id=k, ctx=ast.Load()),
        )

        class_def.body.append(prop_def)

    return class_def


def _get_type_value(
    schema: json_schema.types.AnyOf | json_schema.types.Schema,
) -> ast.Name | ast.Subscript:
    type_value: ast.Name | ast.Subscript

    if isinstance(schema, json_schema.types.AnyOf):
        type_value = _get_union(schema.anyOf)
    else:
        type_value = _get_type_value_for_single_schema(schema)

    return type_value


def _get_union(schemas: list[json_schema.types.Schema]) -> ast.Subscript:
    dims: list[ast.Name] = []
    for schema in schemas:
        if isinstance(schema, json_schema.types.Ref):
            dims.append(ast.Name(id=_convert_schema_id_to_name(schema.ref)))
        else:
            dims.append(convert_json_schema_type_to_ast_name(schema.type))

    return ast.Subscript(
        slice=ast.Tuple(dims=dims),
        value=ast.Name(
            id="Union",
        ),
    )


def _get_type_value_for_single_schema(
    schema: json_schema.types.Schema,
) -> ast.Name:
    if isinstance(schema, json_schema.types.Ref):
        ref_name = schema.ref.split("#")[-1]
        type_value = ast.Name(id=ref_name)
    elif schema.type == "boolean":
        type_value = AstName.bool
    elif schema.type == "integer":
        type_value = AstName.int
    elif schema.type == "number":
        type_value = AstName.float
    elif schema.type == "string":
        type_value = AstName.str
    else:
        raise Exception(f"unexpected property type {schema.type}")

    return type_value

def _convert_schema_id_to_name(value: str) -> str:
    return value.split("#")[-1]
