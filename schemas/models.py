from typing import Generic, TypeVar, Optional, Tuple, Type, Any, List, Dict
from pydantic.utils import GetterDict
from pydantic.generics import GenericModel
from pydantic import (
    BaseModel, PydanticValueError,
    Field, constr, conint, validator, create_model,
)
from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime

Base = declarative_base()


class SimpleUser(BaseModel):
    id: int
    name = "Jane Doe"


class Foo(BaseModel):
    count: int
    size: Optional[float] = None


class Bar(BaseModel):
    apple = "x"
    banana = "y"


class Spam(BaseModel):
    foo: Foo
    bars: List[Bar]


class CompanyOrm(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, nullable=False)
    public_key = Column(String(20), index=True, nullable=False, unique=True)
    name = Column(String(63), unique=True)
    domains = Column(ARRAY(String(255)))


class CompanyModel(BaseModel):
    id: int
    public_key: constr(max_length=20)
    name: constr(max_length=63)
    domains: List[constr(max_length=255)]
    
    class Config:
        orm_mode = True


class SQLModel(Base):
    __tablename__ = "my_table"
    
    id = Column("id", Integer, primary_key=True)
    metadata_ = Column("metadata", JSON)


class ReserveKeyModel(BaseModel):
    metadata: Dict[str, str] = Field(alias="metadata_")
    
    class Config:
        orm_mode = True


class PetClass:
    def __init__(self, *, name: str, species: str):
        self.name = name
        self.species = species


class PersonClass:
    def __init__(self, *, name: str, age: float = None, pets: List[PetClass]):
        self.name = name
        self.age = age
        self.pets = pets


class Pet(BaseModel):
    name: str
    species: str
    
    class Config:
        orm_mode = True


class Person(BaseModel):
    name: str
    age: float = None
    pets: List[Pet]
    
    class Config:
        orm_mode = True


class UserGetter(GetterDict):
    def get(self, key: str, default: Any) -> Any:
        # element attributes
        if key in {"Id", "Status"}:
            return self._obj.attrib.get(key, default)
        # element children
        else:
            try:
                return self._obj.find(key).attrib["Value"]
            except (AttributeError, KeyError):
                return default


class UserGetterModel(BaseModel):
    Id: int
    Status: Optional[str]
    FirstName: Optional[str]
    LastName: Optional[str]
    LoggedIn: bool
    
    class Config:
        orm_mode = True
        getter_dict = UserGetter


class Location(BaseModel):
    lat = 0.1
    lng = 10.1


class Model(BaseModel):
    is_required: float
    gt_int: conint(gt=42)
    list_of_ints: List[int] = None
    a_float: float = None
    recursive_model: Location = None


class NotABarError(PydanticValueError):
    code = "not_a_bar"
    msg_template = 'value is not "bar", got "{wrong_value}"'


class ValidatorModel(BaseModel):
    foo: str
    
    @validator("foo")
    def value_must_equal_bar(cls, v):
        if v != "bar":
            raise NotABarError(wrong_value=v)
        return v


class UserLoginRecord(BaseModel):
    id: int
    name = "John Doe"
    last_login: datetime = None


class TrustedUser(BaseModel):
    id: int
    age: int
    name: str = "John Doe"


class Error(BaseModel):
    code: int
    message: str


class DataModel(BaseModel):
    numbers: List[int]
    people: List[str]


DataT = TypeVar('DataT')


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


TypeX = TypeVar("TypeX")


class BaseClassType(GenericModel, Generic[TypeX]):
    x: TypeX


class ChildClassType(BaseClassType[TypeX], Generic[TypeX]):
    pass


TypeY = TypeVar("TypeY")
TypeZ = TypeVar("TypeZ")


class BaseRootClass(GenericModel, Generic[TypeX, TypeY]):
    x: TypeX
    y: TypeY


class ChildModel(BaseRootClass[int, TypeY], Generic[TypeY, TypeZ]):
    z: TypeZ


class ResponseConcrete(GenericModel, Generic[DataT]):
    data: DataT
    
    @classmethod
    def __concrete_name__(cls: Type[Any], params: Tuple[Type[Any], ...]) -> str:
        return f"{params[0].__name__.title()}Response"


T = TypeVar("T")


class InnerT(GenericModel, Generic[T]):
    inner: T


class OuterT(GenericModel, Generic[T]):
    outer: T
    nested: InnerT[T]


AT = TypeVar("AT")
BT = TypeVar("BT")


class RootModel(GenericModel, Generic[AT, BT]):
    a: AT
    b: BT


DynamicFooBar = create_model("DynamicFooBarModel", foo=(str, ...), bar=123)


class StaticFooBarModel(BaseModel):
    foo: str
    bar: int = 123


class FooModel(BaseModel):
    foo: str
    bar: int = 123


BarModel = create_model(
    "BarModel",
    apple="russet",
    banana="yellow",
    __base__=FooModel,
)


def username_alphanumeric(cls, v):
    assert v.isalnum(), "must be alphanumeric"
    return v


validators = {"username_validator": validator("username")(username_alphanumeric)}


DynamicUserModel = create_model(
    "DynamicUserModel",
    username=(str, ...),
    __validators__=validators,
)
