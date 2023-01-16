from dataclasses import InitVar
from pathlib import Path
from typing import Optional

from pydantic.dataclasses import dataclass


@dataclass
class Birth:
    year: int
    month: int
    day: int


@dataclass
class User:
    birth: Birth

    def __post_init__(self):
        print(self.birth)

    def __post_init_post_parse__(self):
        print(self.birth)


@dataclass
class PathData:
    path: Path
    base_path: InitVar[Optional[Path]]

    def __post_init__(self, base_path):
        print(f"Received path={self.path!r}, base_path={base_path!r}")

    def __post_init_post_parse__(self, base_path):
        if base_path is not None:
            self.path = base_path / self.path


user = User(**{"birth": {"year": 1995, "month": 3, "day": 2}})
print(f"{user = }")

path_data = PathData("world", base_path="/hello")
assert path_data.path == Path("/hello/world")
