from typing import List

from pydantic import BaseModel, ValidationError, validator


class ParentModel(BaseModel):
    names: List[str]


class ChildModel(ParentModel):
    @validator("names", each_item=True)
    def check_names_not_empty(cls, v):
        assert v != "", "empty strings are not allowed"
        return v


class IterativeChildModel(ParentModel):
    @validator("names")
    def check_names_not_empty(cls, v):
        for name in v:
            assert name != "", "empty strings are not allowed"
        return v


try:
    child = ChildModel(names=["Alice", "Bob", "Eve", ""])
except ValidationError as e:
    print(e)
else:
    print("No ValidationError caught.")

try:
    child = IterativeChildModel(names=["Alice", "Bob", "Eve", ""])
except ValidationError as e:
    print(e)
else:
    print("No ValidationError caught.")
