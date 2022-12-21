from typing import List, Union

from pydantic import BaseModel


class Foo(BaseModel):
    pass


class Bar(BaseModel):
    pass


class FaultyModel(BaseModel):
    x: Union[str, int]
    y: Union[Foo, Bar]


class GoodModel(BaseModel):
    x: Union[str, int]
    y: Union[Foo, Bar]

    class Config:
        smart_union = True


class Model(BaseModel, smart_union=True):
    x: Union[List[str], List[int]]


print(f"{FaultyModel(x=1, y=Bar()) = }")

print(f"{GoodModel(x=1, y=Bar()) = }")

print(f"{Model(x=[1, '2']) = }")
print(f"{Model(x=[1, 2]) = }")
