import argparse
import logging

import black

from json_schema_to_python import (
    convert_schemas_to_file_content,
    load_model_schemas,
)

parser = argparse.ArgumentParser()
parser.add_argument(
    "--no-format",
    help="Don't format output",
    action="store_true",
)
parser.add_argument(
    "--input",
    "-i",
    help="Input JSON Schema file path",
    required=True,
)
parser.add_argument("--output", "-o", help="Output Python file path")
parser.add_argument(
    "--silent",
    help="Silence logging",
    action="store_true",
)


def _main(
    *,
    logger: logging.Logger,
    input_path: str,
    output_path: str | None = None,
    should_format: bool,
) -> None:
    schemas = load_model_schemas(logger, input_path)
    content = convert_schemas_to_file_content(schemas)

    if should_format:
        content = black.format_str(content, mode=black.FileMode())

    if output_path is not None:
        with open(output_path, "w+") as f:
            f.write(content)
    else:
        print(content)


def run_cli() -> None:
    args = parser.parse_args()
    logger = logging.getLogger()
    logger.disabled = args.silent

    _main(
        logger=logger,
        input_path=args.input,
        output_path=args.output,
        should_format=args.no_format is not True,
    )
