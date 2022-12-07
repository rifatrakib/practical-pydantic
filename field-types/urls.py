from pydantic import (
    BaseModel,
    HttpUrl,
    PostgresDsn,
    ValidationError,
    validator,
)


class Model(BaseModel):
    url: HttpUrl


class DbModel(BaseModel):
    db: PostgresDsn

    @validator("db")
    def check_db_name(cls, v):
        assert v.path and len(v.path) > 1, "database name must be provided"
        return v


m = Model(url="http://www.example.com")
print(m.url)

try:
    m = Model(url="ftp://invalid.url")
except ValidationError as e:
    print(e)

try:
    m = Model(url="not a url")
except ValidationError as e:
    print(e)


m = Model(url="http://www.example.com")
print(f"{repr(m.url) = }")
print(f"{m.url.scheme = }")
print(f"{m.url.host = }")
print(f"{m.url.host_type = }")
print(f"{m.url.port = }")

m = DbModel(db="postgres://user:pass@localhost:5432/foobar")
print(m.db)

try:
    m = DbModel(db="postgres://user:pass@localhost:5432")
    print(m.db)
except ValidationError as e:
    print(e)

m1 = Model(url="http://puny£code.com")
print(f"{m1.url = }")
print(f"{m1.url.host_type = }")

m2 = Model(url="https://www.аррӏе.com/")
print(f"{m2.url = }")
print(f"{m2.url.host_type = }")

m3 = Model(url="https://www.example.珠宝/")
print(f"{m3.url = }")
print(f"{m3.url.host_type = }")
