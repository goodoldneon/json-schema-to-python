import ast

class AstName:
    bool = ast.Name(id='bool')
    float = ast.Name(id='float')
    int = ast.Name(id='int')
    none = ast.Name(id='None')
    NotRequired = ast.Name(id='NotRequired')
    Optional = ast.Name(id='Optional')
    str = ast.Name(id='str')
    TypedDict = ast.Name(id='TypedDict')
    Union = ast.Name(id='Union')





def convert_json_schema_type_to_ast_name(json_schema_type: str) -> ast.Name:
    _json_schema_type_to_ast_name = {
        "boolean": AstName.bool,
        "integer": AstName.int,
        "null": AstName.none,
        "number": AstName.float,
        "string": AstName.str,
    }

    ast_name = _json_schema_type_to_ast_name.get(json_schema_type)

    if ast_name is None:
        raise Exception(f"cannot convert JSON Schema type {json_schema_type} to ast.Name")

    return ast_name
