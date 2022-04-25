import ast

from .types import AstName


def create_import_nodes() -> list[ast.ImportFrom]:
    """
    Create import ASTs. These are static and will appear in the outputted file
    even if they aren't used.
    """

    future_import = ast.ImportFrom(
        level=0,
        module="__future__",
        names=[AstName.annotations],
    )

    enum_import = ast.ImportFrom(
        level=0,
        module="enum",
        names=[AstName.Enum],
    )

    typing_import = ast.ImportFrom(
        level=0,
        module="typing",
        names=[
            AstName.Literal,
            AstName.Union,
        ],
    )

    typing_extensions_import = ast.ImportFrom(
        level=0,
        module="typing_extensions",
        names=[
            AstName.NotRequired,
            AstName.TypedDict,
        ],
    )

    return [future_import, enum_import, typing_import, typing_extensions_import]
