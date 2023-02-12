from __future__ import annotations

from typing import Any, ForwardRef, List

from pydantic import BaseModel, HttpUrl
from pydantic.errors import ConfigError

Foo = ForwardRef("Foo")


class Model(BaseModel):
    a: List[int]
    b: Any


class Foo(BaseModel):
    a: int = 123
    b: Foo = None


def this_works():
    class Model(BaseModel):
        a: HttpUrl

    print(Model(a="https://example.com"))


def this_is_broken():
    from pydantic import HttpUrl  # HttpUrl is defined in function local scope

    class Model(BaseModel):
        a: HttpUrl

    try:
        Model(a="https://example.com")
    except ConfigError as e:
        print(e)

    try:
        Model.update_forward_refs()
    except NameError as e:
        print(e)


print(Model(a=("1", 2, 3), b="ok"))

Foo.update_forward_refs()
print(Foo())
print(Foo(b={"a": "321"}))

this_works()
this_is_broken()
