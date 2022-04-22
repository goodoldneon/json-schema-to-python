import ast

from .types import Name


def create_imports() -> list[ast.ImportFrom]:
    typing_import = ast.ImportFrom(
        level=0,
        module="typing",
        names=[
            Name.Optional,
            Name.TypedDict,
        ],
    )

    typing_extensions_import = ast.ImportFrom(
        level=0,
        module="typing_extensions",
        names=[Name.NotRequired],
    )

    return [typing_import, typing_extensions_import]
