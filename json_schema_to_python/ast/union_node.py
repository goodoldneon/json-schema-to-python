import ast

from json_schema_to_python import json_schema
from json_schema_to_python.json_schema.types import (
    is_list_of_schemas,
    is_list_of_schema_types,
    SchemaType,
)
from .types import AstName, convert_json_schema_type_to_ast_name


def create_union_node(
    schemas: list[json_schema.types.Schema] | list[SchemaType],
) -> ast.Subscript:
    """
    Create a `Union` AST node
    """

    dims: list[ast.Name] = []

    if is_list_of_schema_types(schemas):
        """
        Example:
            schemas = ["integer", "string"]
        """

        for schema_type in schemas:
            dims.append(convert_json_schema_type_to_ast_name(schema_type))
    elif is_list_of_schemas(schemas):
        """
        Example:
            schemas = [{"type": "integer"}, {"type": "string"}]
        """

        for schema in schemas:
            if isinstance(schema, json_schema.types.AllOfSchema):
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
            elif isinstance(schema, json_schema.types.AnyOfSchema):
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
            elif isinstance(schema, json_schema.types.TypelessSchema):
                """
                Example:

                ```
                {"$ref": "#Foo"}
                ```
                """

                dims.append(ast.Name(id=schema.get_schema_name()))
            elif isinstance(schema.type, list):
                """
                Example:

                ```
                {"type": ["integer", "string"]}
                ```
                """

                for schema_type in schema.type:
                    dims.append(convert_json_schema_type_to_ast_name(schema_type))
            else:
                """
                Example:

                ```
                {"type": "integer"}
                ```
                """

                dims.append(convert_json_schema_type_to_ast_name(schema.type))
    else:
        # Should be unreachable
        raise Exception("unknown type for schemas")

    return ast.Subscript(
        slice=ast.Tuple(dims=dims),
        value=AstName.Union,
    )
