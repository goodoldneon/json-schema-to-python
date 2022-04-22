

from __future__ import annotations

from json_schema_to_model.file import convert_schemas_to_file_content
from json_schema_to_model.json_schema import load_schemas


def main():
    schemas = load_schemas("schema.json")

    with open("output.py", "w+") as f:
        f.write(convert_schemas_to_file_content(schemas))


main()
