from datetime import datetime

from pydantic import Field, ValidationError, validate_arguments
from pydantic.typing import Annotated


@validate_arguments
def how_many(num: Annotated[int, Field(gt=10)]):
    return num


@validate_arguments
def when(dt: datetime = Field(default_factory=datetime.now)):
    return dt


@validate_arguments
def aliased_how_many(num: Annotated[int, Field(gt=10, alias="number")]):
    return num


try:
    m = how_many(1)
except ValidationError as e:
    print(e)

print(type(when()))
print(f"{aliased_how_many(number=42) = }")
