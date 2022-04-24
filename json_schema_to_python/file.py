import ast

from json_schema_to_python.ast import create_module_node
from json_schema_to_python.json_schema.types import Schema


def convert_schemas_to_file_content(schemas: list[Schema]) -> str:
    tree = create_module_node(schemas)

    return ast.unparse(tree)



