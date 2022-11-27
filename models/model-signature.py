import inspect

from pydantic import BaseModel, Field


class FooModel(BaseModel):
    id: int
    name: str = None
    description: str = "Foo"
    apple: int = Field(..., alias="pear")


class MyModel(BaseModel):
    id: int
    info: str = "Foo"

    def __init__(self, id: int = 1, *, bar: str, **data) -> None:
        super().__init__(id=id, bar=bar, **data)


print(f"{inspect.signature(FooModel) = }")
print(f"{inspect.signature(MyModel) = }")
