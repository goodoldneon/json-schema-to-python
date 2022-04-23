import ast

from .types import AstName


def create_imports() -> list[ast.ImportFrom]:
    """
    Create import ASTs. These are static and will appear in the outputted file
    even if they aren't used.
    """

    enum_import = ast.ImportFrom(
        level=0,
        module="enum",
        names=[AstName.Enum],
    )

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

    return [enum_import, typing_import, typing_extensions_import]
