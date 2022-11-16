from typing import List

from pydantic import (
    BaseModel,
    PydanticValueError,
    ValidationError,
    conint,
    validator,
)


class Location(BaseModel):
    lat = 0.1
    lng = 10.1


class Model(BaseModel):
    is_required: float
    gt_int: conint(gt=42)
    list_of_ints: List[int] = None
    a_float: float = None
    recursive_model: Location = None


data = dict(
    list_of_ints=["1", 2, "bad"],
    a_float="not a float",
    recursive_model={"lat": 4.2, "lng": "New York"},
    gt_int=21,
)

try:
    print(Model(**data))
except ValidationError as e:
    print(e)

try:
    print(Model(**data))
except ValidationError as e:
    print(e.json())


class Model(BaseModel):
    foo: str

    @validator("foo")
    def value_must_equal_bar(cls, v):
        if v != "bar":
            raise ValueError("value must be 'bar'")

        return v


try:
    print(Model(foo="ber"))
except ValidationError as e:
    print(e.errors())


class NotABarError(PydanticValueError):
    code = "not_a_bar"
    msg_template = "value is not 'bar', got '{wrong_value}'"


class FooModel(BaseModel):
    foo: str

    @validator("foo")
    def value_must_equal_bar(cls, v):
        if v != "bar":
            raise NotABarError(wrong_value=v)
        return v


try:
    print(Model(foo="ber"))
except ValidationError as e:
    print(e.json())
