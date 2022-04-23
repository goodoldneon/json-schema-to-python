import ast

from json_schema_to_model.ast import create_module
from json_schema_to_model.json_schema.types import Schema


def convert_schemas_to_file_content(schemas: list[Schema]) -> str:
    tree = create_module(schemas)

    return ast.unparse(tree)
