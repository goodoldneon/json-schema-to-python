from __future__ import annotations
from typing import Literal, TypeGuard

import pydantic


SchemaType = Literal[
    "array", "boolean", "integer", "object", "null", "number", "string"
]


class _BaseSchema(pydantic.BaseModel):
    id: str | None = None
    type: SchemaType | None


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


class RootSchema(pydantic.BaseModel):
    properties: dict[str, ObjectSchema]


class StringSchema(_BaseSchema):
    enum: list[str] | None = None
    type: Literal["string"]


class Ref(pydantic.BaseModel):
    ref: str = pydantic.Field(alias="$ref")

    class Config:
        allow_population_by_field_name = True


Schema = (
    Ref
    | AnyOfSchema
    | AllOfSchema
    | ArraySchema
    | BooleanSchema
    | IntegerSchema
    | NullSchema
    | NumberSchema
    | ObjectSchema
    | StringSchema
)
EnumableSchema = IntegerSchema | NumberSchema | StringSchema


def is_enumable_schema(value: Schema) -> TypeGuard[EnumableSchema]:
    return getattr(value, "enum", None) is not None


class AllOf(pydantic.BaseModel):
    __root__: list[Ref]


class AnyOf(pydantic.BaseModel):
    __root__: list[Schema]


AllOf.update_forward_refs()
AllOfSchema.update_forward_refs()
AnyOf.update_forward_refs()
AnyOfSchema.update_forward_refs()
ArraySchema.update_forward_refs()
BooleanSchema.update_forward_refs()
IntegerSchema.update_forward_refs()
NullSchema.update_forward_refs()
NumberSchema.update_forward_refs()
ObjectSchema.update_forward_refs()
Ref.update_forward_refs()
StringSchema.update_forward_refs()
_BaseSchema.update_forward_refs()
