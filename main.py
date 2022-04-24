import argparse

from json_schema_to_python import convert_schemas_to_file_content, load_model_schemas

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", help="Input JSON Schema file path", required=True)
parser.add_argument("--output", "-o", help="Output Python file path")


def main(*, input_path: str, output_path: str | None = None) -> None:
    schemas = load_model_schemas(input_path)
    content = convert_schemas_to_file_content(schemas)

    if output_path is not None:
        with open(output_path, "w+") as f:
            f.write(content)
    else:
        print(content)


if __name__ == "__main__":
    args = parser.parse_args()
    main(input_path=args.input, output_path=args.output)
