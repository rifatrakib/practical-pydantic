from pydantic import BaseModel


class Model(BaseModel):
    a: int
    b: float
    c: str


print(f"{Model(a=3.1415, b=' 2.72 ', c=123) = }")
