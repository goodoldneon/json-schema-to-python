import ast
import textwrap
import unittest

from json_schema_to_python.json_schema.types import Schema, create_schema_from_dict

from .module_node import create_module_node


class Test_create_module_node(unittest.TestCase):
    def assert_module_str(self, schemas: list[Schema], expectation: str):
        # Dedent until at least 1 line is unindented
        expectation = textwrap.dedent(expectation)

        # Remove leading and trailing newlines
        expectation = expectation.strip()

        class_def = create_module_node(schemas)
        assert ast.unparse(class_def) == expectation

    def test_object_and_enum(self) -> None:
        schemas = [
            create_schema_from_dict(
                {
                    "id": "#Animal",
                    "type": "object",
                    "properties": {
                        "is_adorable": {"type": "boolean"},
                        "species": {"$ref": "#Species"},
                        "weight": {"type": "number"},
                    },
                },
            ),
            create_schema_from_dict(
                {
                    "id": "#Pet",
                    "type": "object",
                    "$ref": "#Animal",
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "string"},
                        "toys": {"type": "array", "items": [{"ref": "#Toy"}]},
                    },
                    "required": ["id", "is_adorable", "name", "species", "toys"],
                },
            ),
            create_schema_from_dict(
                {
                    "id": "#Species",
                    "type": "string",
                    "enum": ["cat", "dog"],
                },
            ),
            create_schema_from_dict(
                {
                    "id": "#Toy",
                    "type": "object",
                    "properties": {"is_squeaky": {"type": "boolean"}},
                },
            ),
        ]

        self.assert_module_str(
            schemas,
            """
            from __future__ import annotations
            from enum import Enum
            from typing import Literal, Union
            from typing_extensions import NotRequired, TypedDict

            class Animal(TypedDict):
                is_adorable: NotRequired[bool]
                species: NotRequired[Species]
                weight: NotRequired[float]

            class Pet(Animal):
                id: int
                name: str
                toys: list[Toy]

            class Toy(TypedDict):
                is_squeaky: NotRequired[bool]
            Species = Literal['cat', 'dog']
            """,
        )
