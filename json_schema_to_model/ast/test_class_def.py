import ast
import textwrap
import unittest

from json_schema_to_model.json_schema.types import (
    BooleanSchema,
    IntegerSchema,
    ObjectSchema,
    StringSchema,
)
from .class_def import convert_object_schema_to_class_def


class Test_create_class_def_from_schema(unittest.TestCase):
    def _get_class_str(self, schema: ObjectSchema) -> str:
        class_def = convert_object_schema_to_class_def(schema)
        return ast.unparse(class_def)

    def test_all_types(self) -> None:
        schema = ObjectSchema(
            id="#Person",
            properties={
                "first_name": StringSchema(),
                "last_name": StringSchema(),
                "age": IntegerSchema(),
                "is_active": BooleanSchema(),
            },
            required=["first_name"]
        )

        assert self._get_class_str(schema) == textwrap.dedent("""\
            class Person(TypedDict):
                first_name: str
                last_name: NotRequired[str]
                age: NotRequired[int]
                is_active: NotRequired[bool]"""
        )

