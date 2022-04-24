import ast
import textwrap
import unittest

from json_schema_to_python.json_schema.types import EnumableSchema, StringSchema
from .enum_node import create_enum_node


class Test_create_enum_class_def(unittest.TestCase):
    def _get_class_str(self, schema: EnumableSchema) -> str:
        class_def = create_enum_node(schema)
        return ast.unparse(class_def)

    def test_string_enum(self) -> None:
        """
        Object subschemas become plain dicts. This is because Python doesn't
        support anonymous TypedDicts.
        """

        schema = StringSchema.parse_obj(
            {
                "id": "#Foo",
                "type": "string",
                "enum": ["a", "b"],
            }
        )

        assert self._get_class_str(schema) == textwrap.dedent(
            """\
            Foo = Literal['a', 'b']"""
        )
