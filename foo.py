from typing import TypedDict, Union
from typing_extensions import NotRequired



class Foo(TypedDict):
    a: str | int | bool

class Bar(TypedDict):
    b: NotRequired[Union[str, int, bool]]


class Baz(Foo, Bar):
    pass
