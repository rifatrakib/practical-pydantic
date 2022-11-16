import pickle
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, ValidationError


class User(BaseModel):
    id: int
    name = "John Doe"
    signup_ts: datetime = None


m = User.parse_obj({"id": 123, "name": "James"})
print(m)

try:
    print(User.parse_obj(["not", "a", "dict"]))
except ValidationError as e:
    print(e)

m = User.parse_raw('{"id": 123, "name": "James"}')
print(m)

pickle_data = pickle.dumps(
    {
        "id": 123,
        "name": "James",
        "signup_ts": datetime(2017, 7, 14),
    }
)
m = User.parse_raw(
    pickle_data,
    content_type="application/pickle",
    allow_pickle=True,
)
print(m)

path = Path("data.json")
path.write_text('{"id": 123, "name": "James"}')
m = User.parse_file(path)
print(m)


class NoValidationUser(BaseModel):
    id: int
    age: int
    name: str = "John Doe"


original_user = NoValidationUser(id=123, age=32)
user_data = original_user.dict()
print(user_data)
fields_set = original_user.__fields_set__
print(fields_set)

new_user = NoValidationUser.construct(_fields_set=fields_set, **user_data)
print(repr(new_user))
print(new_user.__fields_set__)

bad_user = NoValidationUser.construct(id="dog")
print(repr(bad_user))
