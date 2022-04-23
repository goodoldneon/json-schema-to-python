import ast
import textwrap
import unittest

from json_schema_to_model.json_schema.types import ObjectSchema
from .class_def import convert_object_schema_to_class_def


class Test_create_class_def_from_schema(unittest.TestCase):
    def _get_class_str(self, schema: ObjectSchema) -> str:
        class_def = convert_object_schema_to_class_def(schema)
        return ast.unparse(class_def)

    def test_all_types(self) -> None:
        schema = ObjectSchema.parse_obj({
            "id": "#Person",
            "properties": {
                "age": {"type": "number"},
                "arms": {"type": "integer"},
                "first_name": {"type": "string"},
                "height": {
                    "anyOf": [
                        {"type": "string"},
                        {"type": "number"},
                        {"type": "null"},
                    ],
                },
                "is_active": {"type": "boolean"},
                "last_name": {"type": "string"},
                "pet": {"$ref": "#Pet"},
                "vehicle": {
                    "anyOf": [{"$ref": "#Bicycle"}, {"$ref": "#Car"}],
                },
            },
            "required": ["first_name"],
            "type": "object",
        })

        assert self._get_class_str(schema) == textwrap.dedent("""\
            class Person(TypedDict):
                age: NotRequired[float]
                arms: NotRequired[int]
                first_name: str
                height: NotRequired[Union[str, float, None]]
                is_active: NotRequired[bool]
                last_name: NotRequired[str]
                pet: NotRequired[Pet]
                vehicle: NotRequired[Union[Bicycle, Car]]"""
        )
