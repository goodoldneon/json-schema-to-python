> 🚧 EXPERIMENTAL 🚧

# JSON Schema to Python

Codegen JSON Schema into Python `TypedDict` classes.

## Examples

```
$ python main.py --input examples/petstore.json
from enum import Enum
from typing import TypedDict, Union
from typing_extensions import NotRequired

class Pet(TypedDict):
    id: int
    name: str
    tag: NotRequired[str]
    species: Species
Species = Literal['cat', 'dog']
```
