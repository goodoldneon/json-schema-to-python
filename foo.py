from typing import Literal, get_args


foos = ["a", "b"]


Foo = Literal["a", "b"]
# Foo = Literal[*foos]


print(get_args(Foo))