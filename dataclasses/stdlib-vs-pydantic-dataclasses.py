import dataclasses
from datetime import datetime
from typing import Optional

import pydantic
from pydantic import BaseModel, ValidationError
from pydantic.dataclasses import dataclass as pydantic_dataclass
from pydantic.dataclasses import set_validation


@dataclasses.dataclass
class Meta:
    modified_date: Optional[datetime]
    seen_count: int


@dataclasses.dataclass
class File(Meta):
    filename: str


@dataclasses.dataclass
class User:
    id: int
    name: str


@dataclasses.dataclass
class Z:
    z: int


@dataclasses.dataclass
class Y(Z):
    y: int = 0


@pydantic.dataclasses.dataclass
class X(Y):
    x: int = 0


@dataclasses.dataclass(frozen=True)
class FrozenUser:
    name: str


@dataclasses.dataclass
class CustomFile:
    filename: str
    last_modification_time: Optional[datetime] = None


class Foo(BaseModel):
    file: CustomFile
    user: Optional[FrozenUser] = None


class ArbitraryType:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"ArbitraryType(value={self.value!r})"


@dataclasses.dataclass
class DC:
    a: ArbitraryType
    b: str


# `ValidatedFile` will be a proxy around `File`
ValidatedFile = pydantic.dataclasses.dataclass(File)

# the original dataclass is the `__dataclass__` attribute
assert ValidatedFile.__dataclass__ is File


validated_file = ValidatedFile(
    filename=b"thefilename",
    modified_date="2020-01-01T00:00",
    seen_count="7",
)
print(f"{validated_file = }")

try:
    item = ValidatedFile(
        filename=["not", "a", "string"],
        modified_date=None,
        seen_count=3,
    )
except pydantic.ValidationError as e:
    print(e)

# `File` is not altered and still does no validation by default
print(
    f"{File(filename=['not', 'a', 'string'], modified_date=None, seen_count=3) = }"
)

# Enhance stdlib dataclass
pydantic_dataclass(User)

user_1 = User(id="whatever", name="I want")

# validate data of `user_1`
try:
    validate = user_1.__pydantic_validate_values__()
except ValidationError as e:
    print(e)

try:
    with set_validation(User, True):
        item = User(id="whatever", name="I want")
except ValidationError as e:
    print(e)

foo = X(x=b"1", y="2", z="3")
print(f"{foo = }")

try:
    item = X(z="pika")
except pydantic.ValidationError as e:
    print(e)

file = CustomFile(
    filename=["not", "a", "string"],
    last_modification_time="2020-01-01T00:00",
)  # nothing is validated as expected
print(f"{file = }")

try:
    item = Foo(file=file)
except ValidationError as e:
    print(e)

foo = Foo(file=CustomFile(filename="myfile"), user=FrozenUser(name="pika"))
try:
    foo.user.name = "bulbi"
except dataclasses.FrozenInstanceError as e:
    print(e)

# valid as it is a builtin dataclass without validation
my_dc = DC(a=ArbitraryType(value=3), b="qwe")

try:

    class Model(pydantic.BaseModel):
        dc: DC
        other: str

    Model(dc=my_dc, other="other")
except RuntimeError as e:  # invalid as it is now a pydantic dataclass
    print(e)


class Model(pydantic.BaseModel):
    dc: DC
    other: str

    class Config:
        arbitrary_types_allowed = True


m = Model(dc=my_dc, other="other")
print(repr(m))
