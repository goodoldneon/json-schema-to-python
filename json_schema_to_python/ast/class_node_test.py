import ast
import textwrap
import unittest

from json_schema_to_python.json_schema.types import ObjectSchema
from .class_node import create_class_node


class Test_create_class_def(unittest.TestCase):
    def assert_class_str(self, schema: ObjectSchema, expectation: str):
        # Dedent until at least 1 line is unindented
        expectation = textwrap.dedent(expectation)

        # Remove leading and trailing newlines
        expectation = expectation.strip()

        class_def = create_class_node(schema)
        assert ast.unparse(class_def) == expectation

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

        self.assert_class_str(
            schema,
            """
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
                string: NotRequired[str]
            """,
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
                    "array_of_multi_type": {
                        "items": [
                            {"type": ["number", "null"]},
                        ],
                        "type": "array",
                    },
                    "array_of_integers_and_multi_type": {
                        "items": [
                            {"type": "integer"},
                            {"type": ["number", "null"]},
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

        self.assert_class_str(
            schema,
            """
            class Foo(TypedDict):
                required_array_of_integers: list[int]
                array_of_integers: NotRequired[list[int]]
                array_of_integers_and_strings: NotRequired[list[Union[int, str]]]
                array_of_multi_type: NotRequired[list[Union[float, None]]]
                array_of_integers_and_multi_type: NotRequired[list[Union[int, float, None]]]
                array_of_refs: NotRequired[list[Bar]]
            """,
        )

    def test_all_of_refs(self) -> None:
        """
        When `allOf` contains only refs, then it should be treated as
        multiple-inheritence
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

        self.assert_class_str(
            schema,
            """
            class Vehicle(Bicycle, Car):
                pass
            """,
        )

    def test_all_of(self) -> None:
        """
        For an `allOf` schema, its ref subschemas should become parent classes
        and its object subschemas should be merged
        """

        schema = ObjectSchema.parse_obj(
            {
                "id": "#Foo",
                "type": "object",
                "allOf": [
                    {"ref": "#Bar"},
                    {"ref": "#Baz"},
                    {
                        "type": "object",
                        "properties": {
                            "a": {"type": "integer"},
                        },
                    },
                    {
                        "type": "object",
                        "properties": {
                            "b": {"type": "integer"},
                        },
                        "required": ["b"],
                    },
                ],
            }
        )

        self.assert_class_str(
            schema,
            """
            class Foo(Bar, Baz):
                a: NotRequired[int]
                b: int
            """,
        )

    def test_any_of_property(self) -> None:
        """
        An `anyOf` property should be treated like a union

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

        self.assert_class_str(
            schema,
            """
            class Person(TypedDict):
                height: Union[str, float, None]
                width: NotRequired[Union[str, float, None]]
                current_vehicle: Union[Bicycle, Car]
                dream_vehicle: NotRequired[Union[Bicycle, Car]]
            """,
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

        self.assert_class_str(
            schema,
            """
            class Foo(TypedDict):
                object: NotRequired[dict]
                array_of_objects: NotRequired[list[dict]]
            """,
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

        self.assert_class_str(
            schema,
            """
            class Foo(TypedDict):
                integers: NotRequired[Literal[1, 2]]
                numbers: NotRequired[Literal[1.1, 1.2]]
                strings: NotRequired[Literal['a', 'b']]
            """,
        )

    def test_multi_type(self) -> None:
        """
        `type` is an array
        """

        schema = ObjectSchema.parse_obj(
            {
                "id": "#Foo",
                "type": "object",
                "properties": {
                    "a": {
                        "type": ["integer", "string"],
                    },
                },
            }
        )

        self.assert_class_str(
            schema,
            """
            class Foo(TypedDict):
                a: NotRequired[Union[int, str]]
            """,
        )

    def test_extend_with_properties(self) -> None:
        """
        Extend another class and also specify properties
        """

        schema = ObjectSchema.parse_obj(
            {
                "id": "#Foo",
                "type": "object",
                "$ref": "#Bar",
                "properties": {
                    "a": {
                        "type": ["integer", "string"],
                    },
                },
            }
        )

        self.assert_class_str(
            schema,
            """
            class Foo(Bar):
                a: NotRequired[Union[int, str]]
            """,
        )
