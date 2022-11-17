from typing import Any, Generic, List, Optional, Tuple, Type, TypeVar

from pydantic import BaseModel, ValidationError, validator
from pydantic.generics import GenericModel

DataT = TypeVar("DataT")


class Error(BaseModel):
    code: int
    message: str


class DataModel(BaseModel):
    numbers: List[int]
    people: List[str]


class Response(GenericModel, Generic[DataT]):
    data: Optional[DataT]
    error: Optional[Error]

    @validator("error", always=True)
    def check_consistency(cls, v, values):
        if v is not None and values["data"] is not None:
            raise ValueError("must not provide both data and error")
        if v is None and values.get("data") is None:
            raise ValueError("must provide data or error")
        return v


data = DataModel(numbers=[1, 2, 3], people=[])
error = Error(code=404, message="Not found")

print(Response[int](data=1))
print(Response[str](data="value"))
print(Response[str](data="value").dict())
print(Response[DataModel](data=data).dict())
print(Response[DataModel](error=error).dict())

try:
    print(Response[int](data="value"))
except ValidationError as e:
    print(e)

TypeX = TypeVar("TypeX")


class BaseClass(GenericModel, Generic[TypeX]):
    X: TypeX


class ChildClass(BaseClass[TypeX], Generic[TypeX]):
    pass


print(ChildClass[int](X=1))

TypeY = TypeVar("TypeY")
TypeZ = TypeVar("TypeZ")


class GenericBaseClass(GenericModel, Generic[TypeX, TypeY]):
    x: TypeX
    y: TypeY


class GenericChildClass(GenericBaseClass[int, TypeY], Generic[TypeY, TypeZ]):
    z: TypeZ


print(GenericChildClass[str, int](x=1, y="y", z=3))


class DataResponse(GenericModel, Generic[DataT]):
    data: DataT

    @classmethod
    def __concrete_name__(
        cls: Type[Any], params: Tuple[Type[Any], ...]
    ) -> str:
        return f"{params[0].__name__.title()}DataResponse"


print(repr(DataResponse[int](data=1)))
print(repr(DataResponse[str](data="a")))

T = TypeVar("T")


class InnerT(GenericModel, Generic[T]):
    inner: T


class OuterT(GenericModel, Generic[T]):
    outer: T
    nested: InnerT[T]


nested = InnerT[int](inner=1)
print(OuterT[int](outer=1, nested=nested))

try:
    nested = InnerT[str](inner="a")
    print(OuterT[int](outer="a", nested=nested))
except ValidationError as e:
    print(e)

AT = TypeVar("AT")
BT = TypeVar("BT")


class Model(GenericModel, Generic[AT, BT]):
    a: AT
    b: BT


print(Model(a="a", b="a"))

IntT = TypeVar("IntT", bound=int)
typevar_model = Model[int, IntT]
print(typevar_model(a=1, b=1))

try:
    typevar_model(a="a", b="a")
except ValidationError as exc:
    print(exc)

concrete_model = typevar_model[int]
print(concrete_model(a=1, b=1))
