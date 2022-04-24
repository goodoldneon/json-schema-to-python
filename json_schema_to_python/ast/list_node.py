import ast

from json_schema_to_python import json_schema
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
        """
        Example:

            ```
            {
                "type": "array",
                "items": [{"type": "integer"}]
            }
            ```
        """

        subschema = schema.items[0]

        if isinstance(subschema, json_schema.types.AllOfSchema):
            """
            Example:
                ```
                {
                    "allOf": [
                        {
                            "allOf": [
                                {"type": "integer"}
                            ]
                        }
                    ]
                }
                ```

            While this is valid JSON Schema, it's pretty bizarre and will
            likely never be supported by this library.
            """

            raise NotImplementedError("nested allOf")
        elif isinstance(subschema, json_schema.types.AnyOfSchema):
            """
            Example:
                ```
                {
                    "anyOf": [
                        {
                            "anyOf": [
                                {"type": "integer"}
                            ]
                        }
                    ]
                }
                ```

            While this is valid JSON Schema, it's pretty bizarre and will
            likely never be supported by this library.
            """

            raise NotImplementedError("nested anyOf")
        elif isinstance(subschema, json_schema.types.RefSchema):
            """
            Example:

            ```
            {"$ref": "#Foo"}
            ```
            """

            slice = ast.Name(id=subschema.get_schema_name())
        elif isinstance(subschema.type, list):
            """
            Example:

                ```
                {
                    "type": "array",
                    "items": [{"type": ["integer", "string"]}]
                }
                ```
            """

            slice = create_union_node(subschema.type)
        else:
            slice = convert_json_schema_type_to_ast_name(subschema.type)
    else:
        """
        Example:

            ```
            {
                "type": "array",
                "items": [
                    {"type": "integer"},
                    {"type": "string"}
                ]
            }
            ```
        """

        slice = create_union_node(schema.items)

    return ast.Subscript(
        slice=slice,
        value=AstName.list,
    )
