import json
import logging
from .types import AnyOfValue, RootSchema, Schema


def _get_schemas_from_root_schema(
    logger: logging.Logger,
    root_schema: RootSchema,
) -> list[Schema]:
    schemas: list[Schema] = []
    for schema in root_schema.properties.values():
        if isinstance(schema, AnyOfValue):
            logger.warn("skipping schema: is anyOf")
            continue

        if schema.id is None:
            logger.warn("skipping schema: no id")
            continue

        schemas.append(schema)

    return schemas


def _load_json_schema(path: str) -> RootSchema:
    with open(path) as f:
        return RootSchema.parse_obj(json.loads(f.read()))


def load_model_schemas(logger: logging.Logger, path: str) -> list[Schema]:
    root_schema = _load_json_schema(path)

    return _get_schemas_from_root_schema(logger, root_schema)
