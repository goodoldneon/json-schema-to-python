import json
from .types import AnyOf, RootSchema, Schema


def _load_json_schema(path: str) -> RootSchema:
    with open(path) as f:
        return RootSchema.parse_obj(json.loads(f.read()))


def load_model_schemas(path: str) -> list[Schema]:
    full_schema = _load_json_schema(path)

    schemas: list[Schema] = []
    for schema in full_schema.properties.values():
        if isinstance(schema, AnyOf):
            raise Exception("anyOf cannot be in the root schema")

        schemas.append(schema)

    return schemas
