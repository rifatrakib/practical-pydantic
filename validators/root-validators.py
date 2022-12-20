from pydantic import BaseModel, ValidationError, root_validator


class UserModel(BaseModel):
    username: str
    password1: str
    password2: str

    @root_validator(pre=True)
    def check_card_number_omitted(cls, values):
        assert (
            "card_number" not in values
        ), "card_number should not be included"
        return values

    @root_validator
    def check_passwords_match(cls, values):
        pw1, pw2 = values.get("password1"), values.get("password2")
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError("passwords do not match")
        return values


print(
    f"{UserModel(username='scolvin', password1='zxcvbn', password2='zxcvbn') = }"  # pragma: allowlist secret
)

try:
    print(
        f"{UserModel(username='scolvin', password1='zxcvbn', password2='zxcvbn2') = }"  # pragma: allowlist secret
    )
except ValidationError as e:
    print(e)

try:
    m = UserModel(
        username="scolvin",
        password1="zxcvbn",  # pragma: allowlist secret
        password2="zxcvbn",  # pragma: allowlist secret
        card_number="1234",
    )
    print(m)
except ValidationError as e:
    print(e)
