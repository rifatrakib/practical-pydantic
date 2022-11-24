from pydantic import BaseModel, ValidationError


class Model(BaseModel):
    a: int
    b = 2
    c: int = 1
    d = 0
    e: float


print(f"{Model.__fields__.keys() = }")

m = Model(e=2, a=1)
print(f"{m.dict() = }")

try:
    item = Model(a="x", b="x", c="x", d="x", e="x")
    print(f"{item = }")
except ValidationError as e:
    error_locations = [e["loc"] for e in e.errors()]
    print(f"{error_locations = }")
