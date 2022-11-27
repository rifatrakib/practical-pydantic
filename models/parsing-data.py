from typing import List

from pydantic import BaseModel, parse_obj_as


class Item(BaseModel):
    id: int
    name: str


item_data = [{"id": 1, "name": "My Item"}]
items = parse_obj_as(List[Item], item_data)
print(items)
