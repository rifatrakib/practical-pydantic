from typing import Annotated
from uuid import uuid4

from pydantic import BaseModel, Field, PositiveInt

try:
    # this won't work since PositiveInt takes precedence over the
    # constraints defined in Field meaning they're ignored
    class NestedModel(BaseModel):
        foo: PositiveInt = Field(..., lt=10)

except ValueError as e:
    print(e)


# but you can set the schema attribute directly:
# (Note: here exclusiveMaximum will not be enforce)
class ExclusiveModel(BaseModel):
    foo: PositiveInt = Field(..., exclusiveMaximum=10)


print(ExclusiveModel.schema())
print(ExclusiveModel.schema_json(indent=4))


# if you find yourself needing this, an alternative is to declare
# the constraints in Field (or you could use conint())
# here both constraints will be enforced:
class Model(BaseModel):
    # Here both constraints will be applied and the schema
    # will be generated correctly
    foo: int = Field(..., gt=0, lt=10)


print(Model.schema())
print(Model.schema_json(indent=4))


class Foo(BaseModel):
    id: Annotated[str, Field(default_factory=lambda: uuid4().hex)]
    name: Annotated[str, Field(max_length=256)] = "Bar"
