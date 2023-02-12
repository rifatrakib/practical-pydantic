from __future__ import annotations

from pydantic import BaseModel


class Foo(BaseModel):
    a: int = 123
    #: The sibling of `Foo` is referenced by string
    sibling: "Foo" = None


class FooModern(BaseModel):
    a: int = 123
    #: The sibling of `FooModern` is referenced directly by type
    sibling: FooModern = None


print(Foo())
print(Foo(sibling={"a": "321"}))

print(FooModern())
print(FooModern(sibling={"a": "321"}))
