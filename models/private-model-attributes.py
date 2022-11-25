from datetime import datetime
from random import randint
from typing import ClassVar

from pydantic import BaseModel, PrivateAttr


class TimeAwareModel(BaseModel):
    _processed_at: datetime = PrivateAttr(default_factory=datetime.utcnow)
    _secret_value: str = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)
        # this could also be done with default_factory
        self._secret_value = randint(1, 5)


m = TimeAwareModel()
print(f"{m._processed_at = }")
print(f"{m._secret_value = }")


class Model(BaseModel):
    _class_var: ClassVar[str] = "class var value"
    _private_attr: str = "private attr value"

    class Config:
        underscore_attrs_are_private = True


print(f"{Model._class_var = }")
print(f"{Model._private_attr = }")
print(f"{Model()._private_attr = }")
