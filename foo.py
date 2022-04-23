from typing import TypedDict, Union
from typing_extensions import NotRequired



class Foo(TypedDict):
    a: list[str | int]
