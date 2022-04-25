# JSON Schema to Python

Codegen JSON Schema into Python `TypedDict` classes.

## 🚧 EXPERIMENTAL 🚧

This project is currently an experiment to see how well JSON Schema can be converted into Python `TypedDict` classes. If it goes well then it'll graduate to a PyPI package.

## Examples

Running this command:

```
python -m json_schema_to_python --input examples/petstore.json
```

Will generate this Python code:

```py
from __future__ import annotations
from enum import Enum
from typing import Literal, TypedDict, Union
from typing_extensions import NotRequired


class Animal(TypedDict):
    is_adorable: NotRequired[bool]
    species: NotRequired[Species]
    weight: NotRequired[float]


class Pet(Animal):
    id: int
    name: str
    toys: list[Toy]


class Toy(TypedDict):
    is_squeaky: NotRequired[bool]


Species = Literal["cat", "dog"]
```

From this JSON Schema:

```json
{
  "id": "#root",
  "properties": {
    "Animal": {
      "id": "#Animal",
      "type": "object",
      "properties": {
        "is_adorable": {
          "type": "boolean"
        },
        "species": {
          "$ref": "#Species"
        },
        "weight": {
          "type": "number"
        }
      }
    },
    "Pet": {
      "id": "#Pet",
      "type": "object",
      "$ref": "#Animal",
      "properties": {
        "id": {
          "type": "integer"
        },
        "name": {
          "type": "string"
        },
        "toys": {
          "type": "array",
          "items": [{ "ref": "#Toy" }]
        }
      },
      "required": ["id", "is_adorable", "name", "species", "toys"]
    },
    "Species": {
      "id": "#Species",
      "type": "string",
      "enum": ["cat", "dog"]
    },
    "Toy": {
      "id": "#Toy",
      "type": "object",
      "properties": {
        "is_squeaky": {
          "type": "boolean"
        }
      }
    }
  }
}
```
