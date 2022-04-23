import ast

class AstName:
    bool = ast.Name(id='bool')
    float = ast.Name(id='float')
    int = ast.Name(id='int')
    NotRequired = ast.Name(id='NotRequired')
    Optional = ast.Name(id='Optional')
    str = ast.Name(id='str')
    TypedDict = ast.Name(id='TypedDict')
    Union = ast.Name(id='Union')
