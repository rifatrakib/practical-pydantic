from pydantic import BaseModel, SecretBytes, SecretStr, ValidationError


class Model(BaseModel):
    password: SecretStr
    password_bytes: SecretBytes


class ModelDumpable(BaseModel):
    password: SecretStr
    password_bytes: SecretBytes

    class Config:
        json_encoders = {
            SecretStr: lambda v: v.get_secret_value() if v else None,
            SecretBytes: lambda v: v.get_secret_value() if v else None,
        }


sm = Model(password="IAmSensitive", password_bytes=b"IAmSensitiveBytes")
print(f"{sm = }")
print(f"{sm.password = }")
print(f"{sm.dict() = }")
print(f"{sm.json() = }")

print(f"{sm.password.get_secret_value() = }")
print(f"{sm.password_bytes.get_secret_value() = }")

try:
    m = Model(password=[1, 2, 3], password_bytes=[1, 2, 3])
    print(m)
except ValidationError as e:
    print(e)


sm = ModelDumpable(
    password="IAmSensitive",
    password_bytes=b"IAmSensitiveBytes",
)
print(f"{sm = }")
print(f"{sm.password = }")
print(f"{sm.dict() = }")
print(f"{sm.json() = }")
