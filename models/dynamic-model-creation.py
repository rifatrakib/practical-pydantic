from pydantic import BaseModel, ValidationError, create_model, validator

DynamicFoobarModel = create_model(
    "DynamicFoobarModel", foo=(str, ...), bar=123
)


class StaticFoobarModel(BaseModel):
    foo: str
    bar: int = 123


class FooModel(BaseModel):
    foo: str
    bar: int = 123


BarModel = create_model(
    "BarModel",
    apple="russet",
    banana="yellow",
    __base__=FooModel,
)

print(BarModel)
print(BarModel.__fields__.keys())


def username_alphanumeric(cls, v):
    assert v.isalnum(), "must be alphanumeric"
    return v


validators = {
    "username_validator": validator("username")(username_alphanumeric)
}

UserModel = create_model(
    "UserModel", username=(str, ...), __validators__=validators
)

user = UserModel(username="scolvin")
print(user)

try:
    print(UserModel(username="scolvi%n"))
except ValidationError as e:
    print(e)
