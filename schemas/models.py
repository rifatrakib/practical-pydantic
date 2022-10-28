from pydantic import BaseModel


class SimpleUser(BaseModel):
    id: int
    name = "Jane Doe"
