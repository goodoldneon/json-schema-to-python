from typing import TypedDict, Union
from typing_extensions import NotRequired



class Foo(TypedDict):
    a: str | int | bool
    b: NotRequired[Union[str, int, bool]]
