from pydantic import ValidationError, create_model_from_typeddict
from typing_extensions import TypedDict


class User(TypedDict):
    name: str
    id: int


class Config:
    extra = "forbid"


UserM = create_model_from_typeddict(User, __config__=Config)
print(repr(UserM(name=123, id="3")))

try:
    print(UserM(name=123, id="3", other="no"))
except ValidationError as e:
    print(e)
