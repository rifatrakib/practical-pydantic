from pydantic import BaseModel, ValidationError, validator


class UserModel(BaseModel):
    name: str
    username: str
    password1: str
    password2: str

    @validator("name")
    def name_must_contain_space(cls, v):
        if " " not in v:
            raise ValueError("must contain a space")
        return v.title()

    @validator("password2")
    def password_match(cls, v, values, **kwargs):
        if "password1" in values and v != values["password1"]:
            raise ValueError("passwords do not match")
        return v

    @validator("username")
    def username_alphanumeric(cls, v):
        assert v.isalnum(), "must be alphanumeric"
        return v


user = UserModel(
    name="samuel colvin",
    username="scolvin",
    password1="zxcvbn",  # pragma: allowlist secret
    password2="zxcvbn",  # pragma: allowlist secret
)
print(f"{user = }")

try:
    user = UserModel(
        name="samuel",
        username="scolvin",
        password1="zxcvbn",  # pragma: allowlist secret
        password2="zxcvbn2",  # pragma: allowlist secret
    )
    print(f"{user = }")
except ValidationError as e:
    print(e)
