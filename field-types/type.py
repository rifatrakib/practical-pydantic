from typing import Type

from pydantic import BaseModel, ValidationError


class Foo:
    pass


class Bar(Foo):
    pass


class Other:
    pass


class SimpleModel(BaseModel):
    just_subclasses: Type[Foo]


class LenientSimpleModel(BaseModel):
    any_class: Type


print(SimpleModel(just_subclasses=Foo))
print(SimpleModel(just_subclasses=Bar))

try:
    m = SimpleModel(just_subclasses=Other)
    print(m)
except ValidationError as e:
    print(e)

print(LenientSimpleModel(any_class=int))
print(LenientSimpleModel(any_class=Foo))

try:
    m = LenientSimpleModel(just_subclasses=Foo())
    print(m)
except ValidationError as e:
    print(e)
