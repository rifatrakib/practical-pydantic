import os
from typing import Any, List

from pydantic import BaseModel, BaseSettings


class DeepSubModel(BaseModel):
    v4: str


class SubModel(BaseModel):
    v1: str
    v2: bytes
    v3: int
    deep: DeepSubModel


class Settings(BaseSettings):
    v0: str
    sub_model: SubModel

    class Config:
        env_nested_delimiter = "__"


class NestedSettings(BaseSettings):
    numbers: List[int]

    class Config:
        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
            if field_name == "numbers":
                return [int(x) for x in raw_val.split(",")]
            return cls.json_loads(raw_val)


os.environ["V0"] = "0"
os.environ["SUB_MODEL"] = '{"v1": "json-1", "v2": "json-2"}'
os.environ["SUB_MODEL__V2"] = "nested-2"
os.environ["SUB_MODEL__V3"] = "3"
os.environ["SUB_MODEL__DEEP__V4"] = "v4"
print(Settings().dict())

os.environ["numbers"] = "1,2,3"
print(NestedSettings().dict())
