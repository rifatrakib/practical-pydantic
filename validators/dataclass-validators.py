from datetime import datetime

from pydantic import validator
from pydantic.dataclasses import dataclass


@dataclass
class DemoDataclass:
    ts: datetime = None

    @validator("ts", pre=True, always=True)
    def set_ts_now(cls, v):
        return v or datetime.now()


print(f"{DemoDataclass() = }")
print(f"{DemoDataclass(ts='2017-11-08T14:00') = }")
