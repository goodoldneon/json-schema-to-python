from __future__ import annotations
from typing import Literal

import pydantic


SchemaType = Literal["boolean", "integer", "object", "string"]


class _BaseSchema(pydantic.BaseModel):
    id: str | None = None
    type: SchemaType


class BooleanSchema(_BaseSchema):
    id: None = None
    type: Literal["boolean"] = "boolean"

class IntegerSchema(_BaseSchema):
    id: None = None
    type: Literal["integer"] = "integer"


class ObjectSchema(_BaseSchema):
    properties: dict[str, Schema]
    required: list[str] = []
    type: Literal["object"] = "object"


class StringSchema(_BaseSchema):
    id: None = None
    type: Literal["string"] = "string"


Schema = BooleanSchema | IntegerSchema | ObjectSchema | StringSchema

ObjectSchema.update_forward_refs()
