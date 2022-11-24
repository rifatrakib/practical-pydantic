import abc

from pydantic import BaseModel


class FooBarModel(BaseModel):
    a: str
    b: int

    @abc.abstractmethod
    def abstract_foobar_method(self):
        pass
