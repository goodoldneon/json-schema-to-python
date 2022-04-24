import unittest


from .merge import _get_schemas_intersection, merge_schemas
from .types import (
    IntegerSchema,
    Schema,
    create_schema_from_dict,
    is_list_of_object_schemas,
)


class Test_merge_schemas(unittest.TestCase):
    def assert_merge_schemas(
        self,
        schemas: list[Schema],
        expectation: dict,
    ) -> None:
        if is_list_of_object_schemas(schemas):
            assert merge_schemas(schemas).to_dict() == expectation

            # Ensure that schema order doesn't matter
            assert merge_schemas(list(reversed(schemas))).to_dict() == expectation
        else:
            raise Exception("schemas is not a list of ObjectSchema")

    def test_no_overlap(self) -> None:
        """
        When properties don't overlap they should both show up in the merged
        schema as-is
        """

        schemas = [
            create_schema_from_dict(
                {
                    "type": "object",
                    "properties": {
                        "a": {"type": "integer"},
                    },
                }
            ),
            create_schema_from_dict(
                {
                    "type": "object",
                    "properties": {
                        "b": {"type": "string"},
                    },
                }
            ),
        ]

        expectation = {
            "type": "object",
            "properties": {
                "a": {"type": "integer"},
                "b": {"type": "string"},
            },
        }

        self.assert_merge_schemas(schemas, expectation)

    def test_overlap_any_of(self) -> None:
        """
        Multi-type properties should have all of their types considered
        """

        schemas = [
            create_schema_from_dict(
                {
                    "type": "object",
                    "properties": {
                        "a": {"type": "integer"},
                        "b": {
                            "anyOf": [
                                {"type": "integer"},
                                {"type": "string"},
                            ],
                        },
                    },
                }
            ),
            create_schema_from_dict(
                {
                    "type": "object",
                    "properties": {
                        "a": {
                            "anyOf": [
                                {"type": "integer"},
                                {"type": "string"},
                            ],
                        },
                        "b": {
                            "anyOf": [
                                {"type": "integer"},
                                {"type": "number"},
                                {"type": "string"},
                            ],
                        },
                    },
                }
            ),
        ]

        expectation = {
            "type": "object",
            "properties": {
                "a": {"type": "integer"},
                "b": {
                    "anyOf": [
                        {"type": "integer"},
                        {"type": "string"},
                    ],
                },
            },
        }

        self.assert_merge_schemas(schemas, expectation)

    def test_overlap_multi_type(self) -> None:
        """
        Multi-type properties should have all of their types considered
        """

        schemas = [
            create_schema_from_dict(
                {
                    "type": "object",
                    "properties": {
                        "a": {"type": "integer"},
                        "b": {"type": ["integer", "string"]},
                    },
                }
            ),
            create_schema_from_dict(
                {
                    "type": "object",
                    "properties": {
                        "a": {"type": ["integer", "string"]},
                        "b": {"type": ["integer", "number", "string"]},
                    },
                }
            ),
        ]

        expectation = {
            "type": "object",
            "properties": {
                "a": {"type": "integer"},
                "b": {
                    "anyOf": [
                        {"type": "integer"},
                        {"type": "string"},
                    ],
                },
            },
        }

        self.assert_merge_schemas(schemas, expectation)

    def test_required(self) -> None:
        """
        Any schema's `required` values should show up in the merged schema
        """

        schemas = [
            create_schema_from_dict(
                {
                    "type": "object",
                    "properties": {
                        "a": {"type": "integer"},
                    },
                }
            ),
            create_schema_from_dict(
                {
                    "type": "object",
                    "properties": {
                        "a": {"type": "integer"},
                    },
                    "required": ["a"],
                }
            ),
        ]

        expectation = {
            "type": "object",
            "properties": {
                "a": {"type": "integer"},
            },
            "required": ["a"],
        }

        self.assert_merge_schemas(schemas, expectation)


class Test_get_schemas_intersection(unittest.TestCase):
    def test_primitives(self) -> None:
        schemas_1 = [create_schema_from_dict({"type": "integer"})]

        schemas_2 = [
            create_schema_from_dict({"type": "integer"}),
            create_schema_from_dict({"type": "string"}),
        ]

        expectation = [IntegerSchema.parse_obj({"type": "integer"})]

        assert _get_schemas_intersection(schemas_1, schemas_2) == expectation

    def test_enums(self) -> None:
        schemas_1 = [
            create_schema_from_dict(
                {
                    "type": "string",
                    "enum": ["a", "b"],
                }
            )
        ]

        schemas_2 = [
            create_schema_from_dict(
                {
                    "type": "string",
                    "enum": ["b", "c"],
                }
            )
        ]

        assert _get_schemas_intersection(schemas_1, schemas_2) == []

    def test_no_intersection(self) -> None:
        schemas_1 = [create_schema_from_dict({"type": "integer"})]
        schemas_2 = [create_schema_from_dict({"type": "string"})]

        assert _get_schemas_intersection(schemas_1, schemas_2) == []
