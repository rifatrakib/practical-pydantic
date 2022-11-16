from typing import Any, Dict, List, Optional
from xml.etree.ElementTree import fromstring

from pydantic import BaseModel, Field, constr
from pydantic.utils import GetterDict
from sqlalchemy import JSON, Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


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


co_orm = CompanyOrm(
    id=123,
    public_key="foobar",
    name="Testing",
    domains=["example.com", "foobar.com"],
)

print(co_orm)

co_model = CompanyModel.from_orm(co_orm)
print(co_model)


class MyModel(BaseModel):
    metadata: Dict[str, str] = Field(alias="metadata_")

    class Config:
        orm_mode = True


class SQLModel(Base):
    __tablename__ = "my_table"
    id = Column("id", Integer, primary_key=True)
    metadata_ = Column("metadata", JSON)


class PetCls:
    def __init__(self, *, name: str, species: str):
        self.name = name
        self.species = species


class PersonCls:
    def __init__(self, *, name: str, age: float = None, pets: List[PetCls]):
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


bones = PetCls(name="Bones", species="dog")
orion = PetCls(name="Orion", species="cat")
anna = PersonCls(name="Anna", age=20, pets=[bones, orion])
anna_model = Person.from_orm(anna)
print(anna_model)

xmlstring = """
<User Id="2138">
    <FirstName />
    <LoggedIn Value="true" />
</User>
"""


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


class User(BaseModel):
    Id: int
    Status: Optional[str]
    FirstName: Optional[str]
    LastName: Optional[str]
    LoggedIn: bool

    class Config:
        orm_mode = True
        getter_dict = UserGetter


user = User.from_orm(fromstring(xmlstring))
print(user)
