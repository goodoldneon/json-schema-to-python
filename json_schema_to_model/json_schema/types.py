from __future__ import annotations
from typing import Literal

import pydantic


SchemaType = Literal["array", "boolean", "integer", "object", "null", "number", "string"]


class _BaseSchema(pydantic.BaseModel):
    id: str | None = None
    type: SchemaType


class ArraySchema(_BaseSchema):
    id: None = None
    items: list[Schema]
    type: Literal["array"]


class BooleanSchema(_BaseSchema):
    id: None = None
    type: Literal["boolean"]


class IntegerSchema(_BaseSchema):
    id: None = None
    type: Literal["integer"]


class NullSchema(_BaseSchema):
    id: None = None
    type: Literal["null"]


class NumberSchema(_BaseSchema):
    id: None = None
    type: Literal["number"]


class ObjectSchema(_BaseSchema):
    allOf: list[Ref] | None = None
    properties: dict[str, AnyOf | Schema] = {}
    required: list[str] = []
    type: Literal["object"]


class StringSchema(_BaseSchema):
    id: None = None
    type: Literal["string"]


class Ref(pydantic.BaseModel):
    ref: str = pydantic.Field(alias='$ref')

    class Config:
        allow_population_by_field_name = True


Schema = Ref | ArraySchema | BooleanSchema | IntegerSchema | NullSchema | NumberSchema | ObjectSchema | StringSchema


class AnyOf(pydantic.BaseModel):
    anyOf: list[Schema]


ArraySchema.update_forward_refs()
ObjectSchema.update_forward_refs()
