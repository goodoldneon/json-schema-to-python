import copy
from typing import TypeVar

from .types import (
    AnyOf,
    AnyOfSchema,
    ObjectSchema,
    Schema,
    get_schema_from_type,
)


def merge_schemas(schemas: list[ObjectSchema]) -> ObjectSchema:
    if len(schemas) == 0:
        return schemas[0]

    new_schema = copy.deepcopy(schemas[0])

    for schema in schemas[1:]:
        for property_name, property_schema in schema.properties.items():
            if property_name in new_schema.properties:
                property_schema = _get_schema_intersection(
                    new_schema.properties[property_name],
                    property_schema,
                )

            new_schema.properties[property_name] = property_schema

            if schema.was_attribute_defaulted("required") is False:
                new_schema.required = list(set(new_schema.required + schema.required))

    return new_schema


def _get_schema_intersection(a: Schema, b: Schema) -> Schema:
    """
    Return a schema that's the intersection of both schema parameters
    """

    # Unable to resolve refs in this function
    if a.ref is not None:
        raise Exception("cannot find intersection for a ref")
    if b.ref is not None:
        raise Exception("cannot find intersection for a ref")

    if isinstance(a, AnyOfSchema):
        a_types = a.anyOf.__root__
    elif a.type is None:
        raise Exception("schema has no type")
    elif isinstance(a.type, list):
        a_types = [get_schema_from_type(type) for type in a.type]
    else:
        a_types = [get_schema_from_type(a.type)]

    if isinstance(b, AnyOfSchema):
        b_types = b.anyOf.__root__
    elif b.type is None:
        raise Exception("schema has no type")
    elif isinstance(b.type, list):
        b_types = [get_schema_from_type(type) for type in b.type]
    else:
        b_types = [get_schema_from_type(b.type)]

    types = _get_schemas_intersection(a_types, b_types)

    if len(types) == 0:
        raise Exception("no schema intersection")
    elif len(types) == 1:
        return types[0]
    else:
        return AnyOfSchema(
            anyOf=AnyOf(
                __root__=types,
            ),
        )


T = TypeVar("T")


def _get_schemas_intersection(a: list[Schema], b: list[Schema]) -> list[Schema]:
    """
    Return a list that contains items that exist in both list parameters.
    Retains list order.
    """

    new_list: list[Schema] = []

    for item in a:
        if item in b:
            new_list.append(item)

    for item in b:
        if item not in new_list and item in a:
            new_list.append(item)

    return new_list
