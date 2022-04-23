import ast
import textwrap
import unittest

from json_schema_to_model.json_schema.types import ObjectSchema
from .class_def import create_class_def


class Test_create_class_def(unittest.TestCase):
    def _get_class_str(self, schema: ObjectSchema) -> str:
        class_def = create_class_def(schema)
        return ast.unparse(class_def)

    def test_basic_types(self) -> None:
        schema = ObjectSchema.parse_obj(
            {
                "id": "#Foo",
                "properties": {
                    "required_boolean": {"type": "boolean"},
                    "boolean": {"type": "boolean"},
                    "required_integer": {"type": "integer"},
                    "integer": {"type": "integer"},
                    "required_null": {"type": "null"},
                    "null": {"type": "null"},
                    "required_number": {"type": "number"},
                    "number": {"type": "number"},
                    "required_object": {"type": "object"},
                    "object": {"type": "object"},
                    "required_ref": {"$ref": "#Bar"},
                    "ref": {"$ref": "#Bar"},
                    "required_string": {"type": "string"},
                    "string": {"type": "string"},
                },
                "required": [
                    "required_boolean",
                    "required_integer",
                    "required_null",
                    "required_number",
                    "required_object",
                    "required_ref",
                    "required_string",
                ],
                "type": "object",
            }
        )

        assert self._get_class_str(schema) == textwrap.dedent(
            """\
            class Foo(TypedDict):
                required_boolean: bool
                boolean: NotRequired[bool]
                required_integer: int
                integer: NotRequired[int]
                required_null: None
                null: NotRequired[None]
                required_number: float
                number: NotRequired[float]
                required_object: dict
                object: NotRequired[dict]
                required_ref: Bar
                ref: NotRequired[Bar]
                required_string: str
                string: NotRequired[str]"""
        )

    def test_array(self) -> None:
        schema = ObjectSchema.parse_obj(
            {
                "id": "#Foo",
                "properties": {
                    "required_array_of_integers": {
                        "items": [
                            {"type": "integer"},
                        ],
                        "type": "array",
                    },
                    "array_of_integers": {
                        "items": [
                            {"type": "integer"},
                        ],
                        "type": "array",
                    },
                    "array_of_integers_and_strings": {
                        "items": [
                            {"type": "integer"},
                            {"type": "string"},
                        ],
                        "type": "array",
                    },
                    "array_of_refs": {
                        "items": [
                            {"$ref": "#Bar"},
                        ],
                        "type": "array",
                    },
                },
                "required": ["required_array_of_integers"],
                "type": "object",
            }
        )

        assert self._get_class_str(schema) == textwrap.dedent(
            """\
            class Foo(TypedDict):
                required_array_of_integers: list[int]
                array_of_integers: NotRequired[list[int]]
                array_of_integers_and_strings: NotRequired[list[Union[int, str]]]
                array_of_refs: NotRequired[list[Bar]]"""
        )

    def test_all_of_keyword(self) -> None:
        """
        The `allOf` keyword should be treated like multiple inheritence

        https://datatracker.ietf.org/doc/html/draft-bhutton-json-schema-00#section-10.2.1.1
        """

        schema = ObjectSchema.parse_obj(
            {
                "id": "#Vehicle",
                "type": "object",
                "allOf": [
                    {"$ref": "#Bicycle"},
                    {"$ref": "#Car"},
                ],
            }
        )

        assert self._get_class_str(schema) == textwrap.dedent(
            """\
            class Vehicle(Bicycle, Car):
                pass"""
        )

    def test_any_of_keyword(self) -> None:
        """
        The `anyOf` keyword should be treated like a union

        https://datatracker.ietf.org/doc/html/draft-bhutton-json-schema-00#section-10.2.1.2
        """

        schema = ObjectSchema.parse_obj(
            {
                "id": "#Person",
                "properties": {
                    "height": {
                        "anyOf": [
                            {"type": "string"},
                            {"type": "number"},
                            {"type": "null"},
                        ],
                    },
                    "width": {
                        "anyOf": [
                            {"type": "string"},
                            {"type": "number"},
                            {"type": "null"},
                        ],
                    },
                    "current_vehicle": {
                        "anyOf": [
                            {"$ref": "#Bicycle"},
                            {"$ref": "#Car"},
                        ],
                    },
                    "dream_vehicle": {
                        "anyOf": [
                            {"$ref": "#Bicycle"},
                            {"$ref": "#Car"},
                        ],
                    },
                },
                "required": ["height", "current_vehicle"],
                "type": "object",
            }
        )

        assert self._get_class_str(schema) == textwrap.dedent(
            """\
            class Person(TypedDict):
                height: Union[str, float, None]
                width: NotRequired[Union[str, float, None]]
                current_vehicle: Union[Bicycle, Car]
                dream_vehicle: NotRequired[Union[Bicycle, Car]]"""
        )

    def test_object_subschema(self) -> None:
        """
        Object subschemas become plain dicts. This is because Python doesn't
        support anonymous TypedDicts.
        """

        schema = ObjectSchema.parse_obj(
            {
                "id": "#Foo",
                "type": "object",
                "properties": {
                    "object": {
                        "type": "object",
                        "properties": {
                            "baz": {"type": "integer"},
                        },
                    },
                    "array_of_objects": {
                        "type": "array",
                        "items": [
                            {
                                "type": "object",
                                "properties": {
                                    "baz": {"type": "integer"},
                                },
                            },
                        ],
                    },
                },
            }
        )

        assert self._get_class_str(schema) == textwrap.dedent(
            """\
            class Foo(TypedDict):
                object: NotRequired[dict]
                array_of_objects: NotRequired[list[dict]]"""
        )

    def test_inline_enum(self) -> None:
        """
        Inline enums become literal unions
        """

        schema = ObjectSchema.parse_obj(
            {
                "id": "#Foo",
                "type": "object",
                "properties": {
                    "integers": {
                        "type": "integer",
                        "enum": [1, 2],
                    },
                    "numbers": {
                        "type": "number",
                        "enum": [1.1, 1.2],
                    },
                    "strings": {
                        "type": "string",
                        "enum": ["a", "b"],
                    },
                },
            }
        )

        assert self._get_class_str(schema) == textwrap.dedent(
            """\
            class Foo(TypedDict):
                integers: NotRequired[Literal[1, 2]]
                numbers: NotRequired[Literal[1.1, 1.2]]
                strings: NotRequired[Literal['a', 'b']]"""
        )
