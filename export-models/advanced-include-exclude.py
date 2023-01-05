import datetime
from typing import List

from pydantic import BaseModel, Field, SecretStr


class User(BaseModel):
    id: int
    username: str
    password: SecretStr


class Transaction(BaseModel):
    id: str
    user: User
    value: int


class Country(BaseModel):
    name: str
    phone_code: int


class Address(BaseModel):
    post_code: int
    country: Country


class CardDetails(BaseModel):
    number: SecretStr
    expires: datetime.date


class Hobby(BaseModel):
    name: str
    info: str


class ComplexUser(BaseModel):
    first_name: str
    second_name: str
    address: Address
    card_details: CardDetails
    hobbies: List[Hobby]


class UserWithConfig(BaseModel):
    id: int
    username: str
    password: SecretStr = Field(..., exclude=True)


class TransactionWithConfig(BaseModel):
    id: str
    user: UserWithConfig = Field(..., exclude={"username"})
    value: int

    class Config:
        fields = {"value": {"exclude": True}}


class UserMergedExclude(BaseModel):
    id: int
    username: str  # overridden by explicit exclude
    password: SecretStr = Field(exclude=True)


class TransactionMergedExclude(BaseModel):
    id: str
    user: UserMergedExclude
    value: int


class UserMergedInclude(BaseModel):
    id: int = Field(..., include=True)
    username: str = Field(..., include=True)  # overridden by explicit include
    password: SecretStr


class TransactionMergedInclude(BaseModel):
    id: str
    user: UserMergedInclude
    value: int


t = Transaction(
    id="1234567890",
    user=User(
        id=42,
        username="JohnDoe",
        password="hashedpassword",  # pragma: allowlist secret
    ),
    value=9876543210,
)

# using a set:
print(f"{t.dict(exclude={'user', 'value'}) = }")

# using a dict:
print(
    f"{t.dict(exclude={'user': {'username', 'password'}, 'value': True}) = }"
)

print(f"{t.dict(include={'id': True, 'user': {'id'}}) = }")

user = ComplexUser(
    first_name="John",
    second_name="Doe",
    address=Address(
        post_code=123456, country=Country(name="USA", phone_code=1)
    ),
    card_details=CardDetails(
        number=4212934504460000, expires=datetime.date(2020, 5, 1)
    ),
    hobbies=[
        Hobby(name="Programming", info="Writing code and stuff"),
        Hobby(name="Gaming", info="Hell Yeah!!!"),
    ],
)

exclude_keys = {
    "second_name": True,
    "address": {"post_code": True, "country": {"phone_code"}},
    "card_details": True,
    # You can exclude fields from specific members of a tuple/list by index:
    "hobbies": {-1: {"info"}},
}

include_keys = {
    "first_name": True,
    "address": {"country": {"name"}},
    "hobbies": {0: True, -1: {"name"}},
}

print(f"{user.dict(include=include_keys) = }")
print(f"{user.dict(exclude={'hobbies': {'__all__': {'info'}}}) = }")

t = TransactionWithConfig(
    id="1234567890",
    user=UserWithConfig(
        id=42,
        username="JohnDoe",
        password="hashedpassword",  # pragma: allowlist secret
    ),
    value=9876543210,
)
print(f"{t.dict() = }")

t = TransactionMergedExclude(
    id="1234567890",
    user=UserMergedExclude(
        id=42,
        username="JohnDoe",
        password="hashedpassword",  # pragma: allowlist secret
    ),
    value=9876543210,
)
print(f"{t.dict(exclude={'value': True, 'user': {'username'}}) = }")

t = TransactionMergedInclude(
    id="1234567890",
    user=UserMergedInclude(
        id=42,
        username="JohnDoe",
        password="hashedpassword",  # pragma: allowlist secret
    ),
    value=9876543210,
)
print(f"{t.dict(include={'id': True, 'user': {'id'}}) = }")
