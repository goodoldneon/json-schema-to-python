import ast
import textwrap
import unittest

from json_schema_to_python.json_schema.types import Schema, create_schema_from_dict

from .module_node import create_module_node


class Test_create_module_node(unittest.TestCase):
    def _get_module_str(self, schemas: list[Schema]) -> str:
        return ast.unparse(create_module_node(schemas))

    def test_object_and_enum(self) -> None:
        schemas = [
            create_schema_from_dict(
                {
                    "id": "#Pet",
                    "required": ["id", "name", "species"],
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "string"},
                        "tag": {"type": "string"},
                        "species": {"$ref": "#Species"},
                    },
                },
            ),
            create_schema_from_dict(
                {
                    "id": "#Species",
                    "type": "string",
                    "enum": ["cat", "dog"],
                },
            ),
        ]

        assert self._get_module_str(schemas) == textwrap.dedent(
            """\
            from enum import Enum
            from typing import TypedDict, Union
            from typing_extensions import NotRequired

            class Pet(TypedDict):
                id: int
                name: str
                tag: NotRequired[str]
                species: Species
            Species = Literal['cat', 'dog']"""
        )
