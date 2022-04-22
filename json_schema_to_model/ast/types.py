import ast

class Name:
    bool = ast.Name(id='bool')
    int = ast.Name(id='int')
    NotRequired = ast.Name(id='NotRequired')
    Optional = ast.Name(id='Optional')
    str = ast.Name(id='str')
    TypedDict = ast.Name(id='TypedDict')
