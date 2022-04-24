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

    bases = [ast.Name(id=s.get_schema_name()) for s in schema.allOf.__root__]

    return ast.ClassDef(
        bases=bases,
        body=[ast.Pass()],
        decorator_list=[],
        keywords=[],
        name=schema.get_schema_name(),
    )
