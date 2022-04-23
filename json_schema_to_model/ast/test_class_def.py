import ast
import textwrap
import unittest

from json_schema_to_model.json_schema.types import ObjectSchema
from .class_def import convert_object_schema_to_class_def


class Test_create_class_def_from_schema(unittest.TestCase):
    def _get_class_str(self, schema: ObjectSchema) -> str:
        class_def = convert_object_schema_to_class_def(schema)
        return ast.unparse(class_def)

    def test_basic_types(self) -> None:
        schema = ObjectSchema.parse_obj({
            "id": "#Foo",
            "properties": {
                "boolean": {"type": "boolean"},
                "optional_boolean": {"type": "boolean"},
                "integer": {"type": "integer"},
                "optional_integer": {"type": "integer"},
                "null": {"type": "null"},
                "optional_null": {"type": "null"},
                "number": {"type": "number"},
                "optional_number": {"type": "number"},
                "object": {"type": "object"},
                "optional_object": {"type": "object"},
                "ref": {"$ref": "#Bar"},
                "optional_ref": {"$ref": "#Bar"},
                "string": {"type": "string"},
                "optional_string": {"type": "string"},
            },
            "required": [
                "boolean",
                "integer",
                "null",
                "number",
                "object",
                "ref",
                "string",
            ],
            "type": "object",
        })

        assert self._get_class_str(schema) == textwrap.dedent("""\
            class Foo(TypedDict):
                boolean: bool
                optional_boolean: NotRequired[bool]
                integer: int
                optional_integer: NotRequired[int]
                null: None
                optional_null: NotRequired[None]
                number: float
                optional_number: NotRequired[float]
                object: dict
                optional_object: NotRequired[dict]
                ref: Bar
                optional_ref: NotRequired[Bar]
                string: str
                optional_string: NotRequired[str]"""
        )

    def test_all_of_keyword(self) -> None:
        """
        The `allOf` keyword should be treated like multiple inheritence
        """

        schema = ObjectSchema.parse_obj({
            "id": "#Vehicle",
            "type": "object",
            "allOf": [
                {"$ref": "#Bicycle"}, {"$ref": "#Car"},
            ],
        })

        assert self._get_class_str(schema) == textwrap.dedent("""\
            class Vehicle(Bicycle, Car):
                pass"""
        )


    def test_any_of_keyword(self) -> None:
        schema = ObjectSchema.parse_obj({
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
        })

        assert self._get_class_str(schema) == textwrap.dedent("""\
            class Person(TypedDict):
                height: Union[str, float, None]
                width: NotRequired[Union[str, float, None]]
                current_vehicle: Union[Bicycle, Car]
                dream_vehicle: NotRequired[Union[Bicycle, Car]]"""
        )