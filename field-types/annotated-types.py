from typing import NamedTuple

from pydantic import BaseModel, Extra, ValidationError
from typing_extensions import TypedDict


class Point(NamedTuple):
    x: int
    y: int


class PointModel(BaseModel):
    p: Point


# `total=False` means keys are non-required
class UserIdentity(TypedDict, total=False):
    name: str
    surname: str


class User(TypedDict):
    identity: UserIdentity
    age: int


class UserModel(BaseModel):
    u: User

    class Config:
        extra = Extra.forbid


print(f"{PointModel(p=('1', '2')) = }")

try:
    m = PointModel(p=("1.3", "2"))
    print(m)
except ValidationError as e:
    print(e)

print(
    f"{UserModel(u={'identity': {'name': 'Smith', 'surname': 'John'}, 'age': '37'}) = }"
)
print(
    f"{UserModel(u={'identity': {'name': None, 'surname': 'John'}, 'age': '37'}) = }"
)
print(f"{UserModel(u={'identity': {}, 'age': '37'}) = }")

try:
    m = UserModel(
        u={"identity": {"name": ["Smith"], "surname": "John"}, "age": "24"}
    )
    print(m)
except ValidationError as e:
    print(e)

try:
    m = UserModel(
        u={
            "identity": {"name": "Smith", "surname": "John"},
            "age": "37",
            "email": "john.smith@me.com",
        }
    )
except ValidationError as e:
    print(e)
