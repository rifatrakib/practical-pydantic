from typing import ClassVar, List, Literal, Optional, Union

from pydantic import BaseModel, ValidationError


class Pie(BaseModel):
    flavor: Literal["apple", "pumpkin"]


class Cake(BaseModel):
    kind: Literal["cake"]
    required_utensils: ClassVar[List[str]] = ["fork", "knife"]


class IceCream(BaseModel):
    kind: Literal["icecream"]
    required_utensils: ClassVar[List[str]] = ["spoon"]


class Meal(BaseModel):
    dessert: Union[Cake, IceCream]


class Dessert(BaseModel):
    kind: str


class SuperPie(BaseModel):
    kind: Literal["pie"]
    flavor: Optional[str]


class ApplePie(Pie):
    flavor: Literal["apple"]


class PumpkinPie(Pie):
    flavor: Literal["pumpkin"]


class DeliciousMeal(BaseModel):
    dessert: Union[ApplePie, PumpkinPie, SuperPie, Dessert]


print(f"{Pie(flavor='apple') = }")
print(f"{Pie(flavor='pumpkin') = }")

try:
    m = Pie(flavor="cherry")
    print(m)
except ValidationError as e:
    print(str(e))

print(f"{type(Meal(dessert={'kind': 'cake'}).dessert).__name__ = }")
print(f"{type(Meal(dessert={'kind': 'icecream'}).dessert).__name__ = }")

try:
    m = Meal(dessert={"kind": "pie"})
    print(m)
except ValidationError as e:
    print(str(e))

print(
    f"{type(DeliciousMeal(dessert={'kind': 'pie', 'flavor': 'apple'}).dessert).__name__ = }"
)
print(
    f"{type(DeliciousMeal(dessert={'kind': 'pie', 'flavor': 'pumpkin'}).dessert).__name__ = }"
)
print(f"{type(DeliciousMeal(dessert={'kind': 'pie'}).dessert).__name__ = }")
print(f"{type(DeliciousMeal(dessert={'kind': 'cake'}).dessert).__name__ = }")
