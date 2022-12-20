from pydantic import BaseModel, validator


def normalize(name: str) -> str:
    return " ".join((word.capitalize()) for word in name.split(" "))


class Producer(BaseModel):
    name: str

    _normalize_name = validator("name", allow_reuse=True)(normalize)


class Consumer(BaseModel):
    name: str

    _normalize_name = validator("name", allow_reuse=True)(normalize)


jane_doe = Producer(name="JaNe DOE")
john_doe = Consumer(name="joHN dOe")
print(f"{jane_doe = }")
print(f"{john_doe = }")
