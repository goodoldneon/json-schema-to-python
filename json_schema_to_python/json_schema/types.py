from __future__ import annotations
from typing import Any, get_args, Literal, TypeGuard

from . import base


SchemaType = Literal[
    "array", "boolean", "integer", "object", "null", "number", "string"
]


class _BaseSchema(base.BaseModel):
    id: str | None = None
    ref: RefValue | None = base.Field(alias="$ref", default=None)
    type: SchemaType | list[SchemaType] | None = None

    def get_schema_name(self) -> str:
        if self.id is None:
            raise Exception("missing id")

        return self.id.split("#")[-1]


class AllOfSchema(_BaseSchema):
    allOf: AllOf
    type: Literal["object"] | None = None


class AnyOfSchema(_BaseSchema):
    anyOf: AnyOf
    type: Literal["object"] | None = None


class ArraySchema(_BaseSchema):
    id: None = None
    items: list[Schema]
    type: Literal["array"]


class BooleanSchema(_BaseSchema):
    id: None = None
    type: Literal["boolean"]


class IntegerSchema(_BaseSchema):
    enum: list[int] | None = None
    type: Literal["integer"]


class MultiTypeSchema(_BaseSchema):
    type: list[SchemaType]


class NullSchema(_BaseSchema):
    id: None = None
    type: Literal["null"]


class NumberSchema(_BaseSchema):
    enum: list[float] | None = None
    type: Literal["number"]


class ObjectSchema(_BaseSchema):
    allOf: AllOf | None = None
    properties: dict[str, Schema] = {}
    required: list[str] = []
    type: Literal["object"]


class RootSchema(base.BaseModel):
    properties: dict[str, Schema]


class StringSchema(_BaseSchema):
    enum: list[str] | None = None
    type: Literal["string"]


class TypelessSchema(base.BaseModel):
    ref: RefValue = base.Field(alias="$ref")
    type: None = None

    class Config:
        allow_population_by_field_name = True

    def get_schema_name(self) -> str:
        return self.ref.__root__.split("#")[-1]


Schema = (
    AllOfSchema
    | AnyOfSchema
    | ArraySchema
    | BooleanSchema
    | IntegerSchema
    | MultiTypeSchema
    | NullSchema
    | NumberSchema
    | ObjectSchema
    | StringSchema
    | TypelessSchema
)
EnumableSchema = IntegerSchema | NumberSchema | StringSchema


def create_schema_from_dict(value: dict) -> Schema:
    for schema_class in get_args(Schema):
        try:
            return schema_class.parse_obj(value)
        except Exception:
            continue

    raise Exception("no schema found")


def get_schema_from_type(type: SchemaType) -> Schema:
    """
    Get a schema object from a schema type string
    """

    for schema_class in get_args(Schema):
        try:
            return schema_class(type=type)
        except Exception:
            continue

    raise Exception(f"no schema found for type {type}")


def is_enumable_schema(value: Schema) -> TypeGuard[EnumableSchema]:
    return getattr(value, "enum", None) is not None


def is_schema(value: Any) -> TypeGuard[Schema]:
    schema_classes = get_args(Schema)

    for schema_class in schema_classes:
        if isinstance(value, schema_class):
            return True

    return False


def is_list_of_object_schemas(
    value: list,
) -> TypeGuard[list[ObjectSchema]]:
    """
    TODO: Make this function accept accept a generic that lets it check for
    arbitrary schemas. Need to wait for a Mypy bug fix:
    https://github.com/python/mypy/pull/11797
    """

    for item in value:
        if isinstance(item, ObjectSchema) is False:
            return False

    return True


def is_list_of_schemas(
    value: list,
) -> TypeGuard[list[Schema]]:
    for item in value:
        if is_schema(item) is False:
            return False

    return True


def is_list_of_schema_types(
    value: list,
) -> TypeGuard[list[SchemaType]]:
    for item in value:
        if item not in get_args(SchemaType):
            return False

    return True


class AllOf(base.BaseModel):
    __root__: list[ObjectSchema | TypelessSchema]


class AnyOf(base.BaseModel):
    __root__: list[Schema]


class RefValue(base.BaseModel):
    __root__: str

    def get_schema_name(self) -> str:
        return self.__root__.split("#")[-1]


AllOf.update_forward_refs()
AllOfSchema.update_forward_refs()
AnyOf.update_forward_refs()
AnyOfSchema.update_forward_refs()
ArraySchema.update_forward_refs()
BooleanSchema.update_forward_refs()
IntegerSchema.update_forward_refs()
MultiTypeSchema.update_forward_refs()
NullSchema.update_forward_refs()
NumberSchema.update_forward_refs()
ObjectSchema.update_forward_refs()
RootSchema.update_forward_refs()
StringSchema.update_forward_refs()
TypelessSchema.update_forward_refs()
_BaseSchema.update_forward_refs()
