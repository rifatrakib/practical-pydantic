import json
from typing import Any, Dict, Type

from pydantic import BaseModel
from pydantic.schema import schema


class Foo(BaseModel):
    a: int


class Model(BaseModel):
    a: Foo


class Person(BaseModel):
    name: str
    age: int

    class Config:
        schema_extra = {
            "examples": [
                {
                    "name": "John Doe",
                    "age": 25,
                }
            ]
        }


class ComplexPerson(BaseModel):
    name: str
    age: int

    class Config:
        @staticmethod
        def schema_extra(
            schema: Dict[str, Any], model: Type["Person"]
        ) -> None:
            for prop in schema.get("properties", {}).values():
                prop.pop("title", None)


# Default location for OpenAPI
top_level_schema = schema([Model], ref_prefix="#/components/schemas/")
print(json.dumps(top_level_schema, indent=2))

print(Person.schema_json(indent=2))

print(ComplexPerson.schema_json(indent=2))
