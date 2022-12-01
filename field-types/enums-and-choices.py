from enum import Enum, IntEnum

from pydantic import BaseModel, ValidationError


class FruitEnum(str, Enum):
    pear = "pear"
    banana = "banana"


class ToolEnum(IntEnum):
    spanner = 1
    wrench = 2


class CookingModel(BaseModel):
    fruit: FruitEnum = FruitEnum.pear
    tool: ToolEnum = ToolEnum.spanner


print(CookingModel())
print(CookingModel(tool=2, fruit="banana"))

try:
    m = CookingModel(fruit="other")
    print(m)
except ValidationError as e:
    print(e)
