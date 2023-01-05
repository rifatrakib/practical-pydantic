from datetime import date, datetime, timedelta
from typing import List, Optional

import orjson
import ujson
from pydantic import BaseModel
from pydantic.json import timedelta_isoformat
from pydantic.validators import int_validator


def orjson_dumps(v, *, default):
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(v, default=default).decode()


class BarModel(BaseModel):
    whatever: int


class FooBarModel(BaseModel):
    foo: datetime
    bar: BarModel


class WithCustomEncoders(BaseModel):
    dt: datetime
    diff: timedelta

    class Config:
        json_encoders = {
            datetime: lambda v: v.timestamp(),
            timedelta: timedelta_isoformat,
        }


class BaseClassWithEncoders(BaseModel):
    dt: datetime
    diff: timedelta

    class Config:
        json_encoders = {datetime: lambda v: v.timestamp()}


class ChildClassWithEncoders(BaseClassWithEncoders):
    class Config:
        json_encoders = {timedelta: timedelta_isoformat}


class Address(BaseModel):
    city: str
    country: str


class User(BaseModel):
    name: str
    address: Address
    friends: Optional[List["User"]] = None

    class Config:
        json_encoders = {
            Address: lambda a: f"{a.city} ({a.country})",
            "User": lambda u: f"{u.name} in {u.address.city} "
            f"({u.address.country[:2].upper()})",
        }


class DayThisYear(date):
    """Contrived example of a special type of date that takes an int and
    interprets it as a day in the current year."""

    @classmethod
    def __get_validators__(cls):
        yield int_validator
        yield cls.validate

    @classmethod
    def validate(cls, v: int):
        return date.today().replace(month=1, day=1) + timedelta(days=v)


class FooModel(BaseModel):
    date: DayThisYear


class UjsonUser(BaseModel):
    id: int
    name = "John Doe"
    signup_ts: datetime = None

    class Config:
        json_loads = ujson.loads


class OrjsonUser(BaseModel):
    id: int
    name = "John Doe"
    signup_ts: datetime = None

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


User.update_forward_refs()


m = FooBarModel(foo=datetime(2032, 6, 1, 12, 13, 14), bar={"whatever": 123})
print(f"{m.json() = }")

m = WithCustomEncoders(dt=datetime(2032, 6, 1), diff=timedelta(hours=100))
print(f"{m.json() = }")

m = ChildClassWithEncoders(dt=datetime(2032, 6, 1), diff=timedelta(hours=100))
print(f"{m.json() = }")

wolfgang = User(
    name="Wolfgang",
    address=Address(city="Berlin", country="Deutschland"),
    friends=[
        User(name="Pierre", address=Address(city="Paris", country="France")),
        User(name="John", address=Address(city="London", country="UK")),
    ],
)
print(f"{wolfgang.json(models_as_dict=False) = }")

m = FooModel(date=300)
print(f"{m.json() = }")

user = UjsonUser.parse_raw(
    '{"id": 123,"signup_ts":1234567890,"name":"John Doe"}'
)
print(f"{user = }")

user = OrjsonUser.parse_raw(
    '{"id":123,"signup_ts":1234567890,"name":"John Doe"}'
)
print(f"{user.json() = }")
