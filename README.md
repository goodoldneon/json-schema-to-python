# JSON Schema to Python

Codegen JSON Schema into Python `TypedDict` classes.

## 🚧 EXPERIMENTAL 🚧

This project is currently an experiment to see how well JSON Schema can be converted into Python `TypedDict` classes. If it goes well then it'll graduate to a PyPI package.

## Examples

```
$ python -m json_schema_to_python --input examples/petstore.json
from __future__ import annotations
from enum import Enum
from typing import Literal, TypedDict, Union
from typing_extensions import NotRequired


class Pet(TypedDict):
    id: int
    is_adorable: bool
    name: str
    species: Species
    toys: list[Toy]
    weight: NotRequired[float]


class Toy(TypedDict):
    is_squeeky: NotRequired[bool]


Species = Literal["cat", "dog"]
```
