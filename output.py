from enum import Enum
from typing import TypedDict, Union
from typing_extensions import NotRequired

class Person(TypedDict):
    first_name: str
    last_name: NotRequired[str]
    age: NotRequired[int]
    vehicle: Union[Bike, Car]

class Bike(TypedDict):
    frame: str

class Car(TypedDict):
    color: str