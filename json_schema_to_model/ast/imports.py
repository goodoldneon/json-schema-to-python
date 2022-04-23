import ast

from .types import AstName


def create_imports() -> list[ast.ImportFrom]:
    typing_import = ast.ImportFrom(
        level=0,
        module="typing",
        names=[
            AstName.Optional,
            AstName.TypedDict,
            AstName.Union,
        ],
    )

    typing_extensions_import = ast.ImportFrom(
        level=0,
        module="typing_extensions",
        names=[AstName.NotRequired],
    )

    return [typing_import, typing_extensions_import]
