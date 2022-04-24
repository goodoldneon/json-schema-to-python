import ast


class AstName:
    annotations = ast.Name(id="annotations")
    bool = ast.Name(id="bool")
    dict = ast.Name(id="dict")
    Enum = ast.Name(id="Enum")
    float = ast.Name(id="float")
    int = ast.Name(id="int")
    list = ast.Name(id="list")
    Literal = ast.Name(id="Literal")
    none = ast.Name(id="None")
    NotRequired = ast.Name(id="NotRequired")
    Optional = ast.Name(id="Optional")
    str = ast.Name(id="str")
    TypedDict = ast.Name(id="TypedDict")
    Union = ast.Name(id="Union")


def convert_json_schema_type_to_ast_name(json_schema_type: str) -> ast.Name:
    _json_schema_type_to_ast_name = {
        "boolean": AstName.bool,
        "object": AstName.dict,
        "integer": AstName.int,
        "null": AstName.none,
        "number": AstName.float,
        "string": AstName.str,
    }

    ast_name = _json_schema_type_to_ast_name.get(json_schema_type)

    if ast_name is None:
        raise Exception(
            f"cannot convert JSON Schema type {json_schema_type} to ast.Name"
        )

    return ast_name
