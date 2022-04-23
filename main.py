from json_schema_to_model import convert_schemas_to_file_content, load_model_schemas


def main():
    schemas = load_model_schemas("schema.json")

    with open("output.py", "w+") as f:
        f.write(convert_schemas_to_file_content(schemas))


main()
