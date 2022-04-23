import ast
import textwrap
import unittest

from json_schema_to_model.json_schema.types import (
    AnyOf,
    BooleanSchema,
    IntegerSchema,
    ObjectSchema,
    Ref,
    StringSchema,
)
from .class_def import convert_object_schema_to_class_def
foo: float = 1.1

class Test_create_class_def_from_schema(unittest.TestCase):
    def _get_class_str(self, schema: ObjectSchema) -> str:
        class_def = convert_object_schema_to_class_def(schema)
        return ast.unparse(class_def)

    def test_all_types(self) -> None:
        schema = ObjectSchema.parse_obj({
            "id": "#Person",
            "properties": {
                "first_name": {"type": "string"},
                "last_name": {"type": "string"},
                "age": {"type": "number"},
                "arms": {"type": "integer"},
                "is_active": {"type": "boolean"},
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
                first_name: str
                last_name: NotRequired[str]
                age: NotRequired[float]
                arms: NotRequired[int]
                is_active: NotRequired[bool]
                pet: NotRequired[Pet]
                vehicle: NotRequired[Union[Bicycle, Car]]"""
        )
