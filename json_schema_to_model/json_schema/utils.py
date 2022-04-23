def convert_schema_id_to_name(value: str) -> str:
    return value.split("#")[-1]
