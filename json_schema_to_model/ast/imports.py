import ast

from .types import AstName


def create_imports() -> list[ast.ImportFrom]:
    """
    Create import ASTs. These are static and will appear in the outputted file
    even if they aren't used.
    """

    typing_import = ast.ImportFrom(
        level=0,
        module="typing",
        names=[
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
