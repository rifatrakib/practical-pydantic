from pydantic import BaseModel


class BarModel(BaseModel):
    whatever: int


class FooBarModel(BaseModel):
    banana: float
    foo: str
    bar: BarModel


m = FooBarModel(banana=3.14, foo="hello", bar={"whatever": 123})

print(f"{m.copy(include={'foo', 'bar'}) = }")
print(f"{m.copy(exclude={'foo', 'bar'}) = }")
print(f"{m.copy(update={'banana': 0}) = }")
print(f"{id(m.bar), (m.copy().bar) = }")
print(f"{id(m.bar), (m.copy(deep=True).bar) = }")
