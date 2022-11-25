from typing import Optional

from pydantic import BaseModel, Field, ValidationError


class Model(BaseModel):
    a: int
    b: int = ...
    c: int = Field(...)


class OptionalRequiredModel(BaseModel):
    a: Optional[int]
    b: Optional[int] = ...
    c: Optional[int] = Field(...)


print(f"{OptionalRequiredModel(b=1, c=2) = }")

try:
    print(f"{OptionalRequiredModel(a=1, b=2) = }")
except ValidationError as e:
    print(e)
