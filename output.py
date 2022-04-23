from typing import Optional, TypedDict
from typing_extensions import NotRequired

class Person(TypedDict):
    first_name: str
    last_name: NotRequired[str]
    age: NotRequired[int]
    car: NotRequired[Car]

class Car(TypedDict):
    color: str