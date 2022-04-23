from typing import Optional, TypedDict, Union
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