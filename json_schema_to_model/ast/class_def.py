import ast

from json_schema_to_model import json_schema
from .types import Name

def convert_object_schema_to_class_def(
    schema: json_schema.types.ObjectSchema,
) -> ast.ClassDef:
    """
    Convert a
    """

    assert schema.id is not None
    name = schema.id.split("#")[-1]

    class_def = ast.ClassDef(
        bases=[Name.TypedDict],
        body=[],
        decorator_list=[],
        keywords=[],
        name=name,
    )

    for k, v in schema.properties.items():
        if v.type == "boolean":
            type_value = Name.bool
        elif v.type == "integer":
            type_value = Name.int
        elif v.type == "string":
            type_value = Name.str
        else:
            raise Exception(f"unexpected property type {v.type}")

        if k in schema.required:
            annotation: ast.Name | ast.Subscript = type_value
        else:
            annotation = ast.Subscript(
                slice=type_value,
                value=Name.NotRequired,
            )

        prop_def = ast.AnnAssign(
            annotation=annotation,
            simple=1,
            target=ast.Name(id=k, ctx=ast.Load()),
        )

        class_def.body.append(prop_def)

    return class_def