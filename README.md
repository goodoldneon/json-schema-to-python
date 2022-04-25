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

## Known Limitations

### `id` is required

This is primarily to simplify the library. It isn't impossible to avoid using `id`, but the extra complexity doesn't seem worthwhile.

The primary reason for this decision is to avoid messy class name issues. For example, if you had schemas in `#properties/foo/Thing` and `#properties/bar/Thing` then what would you call each? `FooThing` and `BarThing`? And what would happen if you had another schema whose `id` was already `FooThing`? Adding class name magic is a can of worms, so it seems best to avoid it by using explicit class names via `id`.

### Nested `object` schemas just become type `dict`

This is because Mypy doesn't support anonymous `TypedDict`s (see [this discussion](https://github.com/python/mypy/issues/9884)).

If we had this schema:

```json
{
  "id": "#root",
  "properties": {
    "Foo": {
      "properties": {
        "bar": {
          "type": "object",
          "properties": {
            "baz": { "type": "integer" }
          }
        }
      }
    }
  }
}
```

Then it'd be nice to generate something like this:

```py
Foo = TypedDict(
    {
        "bar": {
            {"baz": int},
        },
    },
)
```

But that's impossible right now.

### `additionalProperties` is ignored

This is because `TypedDict` has spotty support "extra" keys during dict creation (see [this discussion](https://github.com/python/mypy/issues/4617)). Sometimes Mypy is OK with extra keys and sometimes it isn't:

```py
class Foo(TypedDict):
    a: int

class Bar(TypedDict):
    a: int
    b: int

# Mypy error when declaring a dict with extra keys
foo: Foo = {"a": 1, "b": 2}

bar: Bar = {"a": 1, "b": 2}

def stuff(value: Foo) -> None:
    pass

# No Mypy error when passing a dict variable with extra keys
stuff(bar)

# Mypy error when passing an anonymous dict with extra keys
stuff({"a": 1, "b": 2})
```

### JSON Schema enums become Python `Literal`s (not `Enum`s)

This is because Python `Enum` members are actually objects and not primitives:

```
>>> from enum import Enum
>>> class Foo(Enum):
...     a = "a"
...
>>> Foo.a
<Foo.a: 'a'>
>>> Foo.a.value
'a'
```

That won't match your runtime data if you just did a `json.loads` on a request body.
