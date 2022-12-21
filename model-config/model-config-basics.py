from datetime import datetime

from pydantic import BaseModel, Extra, ValidationError
from pydantic.dataclasses import dataclass


class SimpleModel(BaseModel):
    v: str

    class Config:
        max_anystr_length = 10
        error_msg_templates = {
            "value_error.any_str.max_length": "max_length: {limit_value}",
        }


class ExtraModel(BaseModel, extra=Extra.forbid):
    a: str


class MyConfig:
    max_anystr_length = 10
    validate_assignment = True
    error_msg_templates = {
        "value_error.any_str.max_length": "max_length: {limit_value}",
    }


@dataclass(config=MyConfig)
class User:
    id: int
    name: str = "John Doe"
    signup_ts: datetime = None


try:
    m = SimpleModel(v="x" * 20)
    print(m)
except ValidationError as e:
    print(e)

try:
    m = ExtraModel(a="spam", b="oh no")
    print(m)
except ValidationError as e:
    print(e)

user = User(id="42", signup_ts="2032-06-21T12:00")
try:
    user.name = "x" * 20
except ValidationError as e:
    print(e)
