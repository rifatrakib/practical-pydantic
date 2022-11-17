import json
from typing import Dict, List

from pydantic import BaseModel, ValidationError
from pydantic.schema import schema


class Pets(BaseModel):
    __root__: List[str]


print(Pets(__root__=["dog", "cat"]))
print(Pets(__root__=["dog", "cat"]).json())
print(Pets.parse_obj(["dog", "cat"]))
print(Pets.schema())

pets_schema = schema([Pets])
print(json.dumps(pets_schema, indent=2))

print(Pets.parse_obj(["dog", "cat"]))
print(Pets.parse_obj({"__root__": ["dog", "cat"]}))  # not recommended


class PetsByName(BaseModel):
    __root__: Dict[str, str]


print(PetsByName.parse_obj({"Otis": "dog", "Milo": "cat"}))

try:
    print(PetsByName.parse_obj({"__root__": {"Otis": "dog", "Milo": "cat"}}))
except ValidationError as e:
    print(e)


class MappedPets(BaseModel):
    __root__: List[str]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]


pets = MappedPets.parse_obj(["dog", "cat"])
print(pets[0])
print([pet for pet in pets])
