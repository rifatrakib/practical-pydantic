from pydantic import BaseModel, ValidationError
from pydantic.color import Color


class Model(BaseModel):
    color: Color


c = Color("ff00ff")
print(f"{c.as_named() = }")
print(f"{c.as_hex() = }")

c = Color("green")
print(f"{c.as_rgb_tuple() = }")
print(f"{c.original() = }")

print(f"{repr(Color('hsl(180, 100%, 50%)')) = }")

print(f"{Model(color='purple') = }")

try:
    print(f"{Model(color='hello') = }")
except ValidationError as e:
    print(e)
