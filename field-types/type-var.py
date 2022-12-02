from typing import TypeVar

from pydantic import BaseModel

FooBar = TypeVar("FooBar")
BoundFloat = TypeVar("BoundFloat", bound=float)
IntStr = TypeVar("IntStr", int, str)


class Model(BaseModel):
    a: FooBar  # equivalent of ": Any"
    b: BoundFloat  # equivalent of ": float"
    c: IntStr  # equivalent of ": Union[int, str]"


print(Model(a=[1], b=4.2, c="x"))
print(Model(b=1, c=1))
