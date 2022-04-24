import ast

from json_schema_to_python import json_schema
from .attribute_node import get_attribute_node
from .types import AstName


def create_class_node(
    schema: json_schema.types.ObjectSchema,
) -> ast.ClassDef:
    """
    Create a `Class` AST node for a model
    """

    if schema.allOf:
        return _create_class_node_using_all_of(schema)

    class_def = ast.ClassDef(
        bases=[AstName.TypedDict],
        body=[],
        decorator_list=[],
        keywords=[],
        name=schema.get_schema_name(),
    )

    for k, v in schema.properties.items():
        class_def.body.append(
            get_attribute_node(
                property_name=k,
                property_schema=v,
                is_required=k in schema.required,
            )
        )

    return class_def


def _create_class_node_using_all_of(
    schema: json_schema.types.ObjectSchema,
) -> ast.ClassDef:
    """
    If an object schema uses the `allOf` keyword, then use multiple inheritence
    for all of the refs in `allOf`.

    This solution is not fully JSON Schema compliant. For example, it won't
    support schemas that specify both `allOf` and `required`:

    ```
    {
        "id": "#Foo",
        "type": "object",
        "allOf": [{"$ref": "Bar"}, {"$ref": "Baz"}],
        "required": ["name"]
    }
    ```

    The only way to support using both `allOf` and `required` is to stop using
    multiple inheritence and merge the schemas before creating the ClassDef.
    This can be done but would take some work.
    """

    assert schema.allOf is not None
    assert schema.id is not None

    class_node: ast.ClassDef
    subschemas = schema.allOf.__root__
    bases: list[ast.expr] = []
    body: list[ast.stmt] = []
    subschemas_to_merge: list[json_schema.types.ObjectSchema] = []

    for subschema in subschemas:
        if isinstance(subschema, json_schema.types.Ref):
            bases.append(ast.Name(id=subschema.get_schema_name()))
        elif isinstance(subschema, json_schema.types.ObjectSchema):
            subschemas_to_merge.append(subschema)

    if len(bases) == 0:
        bases = [AstName.TypedDict]

    if len(subschemas_to_merge) == 0:
        body = [ast.Pass()]
    else:
        merged_subschemas = json_schema.merge_schemas(subschemas_to_merge)

        for k, v in merged_subschemas.properties.items():
            body.append(
                get_attribute_node(
                    property_name=k,
                    property_schema=v,
                    is_required=k in merged_subschemas.required,
                )
            )

    class_node = ast.ClassDef(
        bases=bases,
        body=body,
        decorator_list=[],
        keywords=[],
        name=schema.get_schema_name(),
    )

    return class_node
