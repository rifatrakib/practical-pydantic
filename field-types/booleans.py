from pydantic import BaseModel, ValidationError


class BooleanModel(BaseModel):
    bool_value: bool


print(BooleanModel(bool_value=False))
print(BooleanModel(bool_value="False"))

try:
    m = BooleanModel(bool_value=[])
    print(m)
except ValidationError as e:
    print(str(e))
