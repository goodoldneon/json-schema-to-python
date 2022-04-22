from typing import Optional, TypedDict
from typing_extensions import NotRequired

class Person(TypedDict):
    first_name: NotRequired[str]