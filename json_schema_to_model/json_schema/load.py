import json
from .types import AnyOf, ObjectSchema, Schema

def _load_json_schema(path: str) -> ObjectSchema:
    with open(path) as f:
        return ObjectSchema.parse_obj(json.loads(f.read()))


def load_schemas(path: str) -> list[Schema]:
    full_schema = _load_json_schema(path)

    schemas: list[Schema] = []
    for schema in full_schema.properties.values():
        if isinstance(schema, AnyOf):
            raise Exception("anyOf cannot be in the root schema")

        schemas.append(schema)

    return schemas
