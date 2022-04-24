from typing import Any
import pydantic


class BaseModel(pydantic.BaseModel):
    def to_dict(self) -> dict[str, Any]:
        # Don't include any keys whose values haven't been explicitly set. In
        # other words, leave out defaulted attributes.
        exclude_unset = True

        return self.dict(exclude_unset=exclude_unset)

    def was_attribute_defaulted(self, name: str) -> bool:
        """
        Check whether attribute was defaulted. This happens when an attribute is
        never set.

        Args:
            name: Attribute name
        """

        return name not in self.__fields_set__


Field = pydantic.Field
