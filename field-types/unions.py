from typing import Literal, Union
from uuid import UUID

from pydantic import BaseModel, Field, ValidationError
from typing_extensions import Annotated


class User(BaseModel):
    id: Union[int, str, UUID]
    name: str


class RightUser(BaseModel):
    id: Union[UUID, int, str]
    name: str


class Cat(BaseModel):
    pet_type: Literal["cat"]
    meows: int


class Dog(BaseModel):
    pet_type: Literal["dog"]
    barks: int


class Lizard(BaseModel):
    pet_type: Literal["reptile", "lizard"]
    scales: bool


class Pet(BaseModel):
    pet: Union[Cat, Dog, Lizard] = Field(..., discrimintor="pet_type")
    n: int


class BlackCat(BaseModel):
    pet_type: Literal["cat"]
    color: Literal["black"]
    black_name: str


class WhiteCat(BaseModel):
    pet_type: Literal["cat"]
    color: Literal["white"]
    white_name: str


user_1 = User(id=123, name="John Doe")
print(user_1)
print(user_1.id)

user_2 = User(id="1234", name="John Doe")
print(user_2)
print(user_2.id)

user_3_uuid = UUID("cf57432e-809e-4353-adbd-9d5c0d733868")
user_3 = User(id=user_3_uuid, name="John Doe")
print(user_3)
print(user_3.id)
print(user_3_uuid.int)

user_3_uuid = UUID("cf57432e-809e-4353-adbd-9d5c0d733868")
user_3 = RightUser(id=user_3_uuid, name="John Doe")
print(user_3)
print(user_3.id)
print(user_3_uuid.int)

print(f"{Pet(pet={'pet_type': 'dog', 'barks': 3.14}, n=1) = }")

try:
    print(f"{Pet(pet={'pet_type': 'dog'}, n=1) = }")
except ValidationError as e:
    print(e)

# # Can also be written with a custom root type
# class ColoredCat(BaseModel):
#     __root__: Annotated[Union[BlackCat, WhiteCat], Field(discriminator="color")]
ColoredCat = Annotated[Union[BlackCat, WhiteCat], Field(discriminator="color")]
UpgragedPet = Annotated[
    Union[ColoredCat, Dog], Field(discriminator="pet_type")
]


class Model(BaseModel):
    pet: UpgragedPet
    n: int


m = Model(
    pet={"pet_type": "cat", "color": "black", "black_name": "felix"}, n=1
)
print(m)

try:
    m = Model(pet={"pet_type": "cat", "color": "red"}, n="1")
    print(m)
except ValidationError as e:
    print(e)

try:
    m = Model(pet={"pet_type": "cat", "color": "black"}, n="1")
    print(m)
except ValidationError as e:
    print(e)
