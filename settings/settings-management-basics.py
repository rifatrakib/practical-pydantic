from typing import Set

from pydantic import (
    AmqpDsn,
    BaseModel,
    BaseSettings,
    Field,
    PostgresDsn,
    PyObject,
    RedisDsn,
)


class SubModel(BaseModel):
    foo = "bar"
    apple = 1


class Settings(BaseSettings):
    auth_key: str
    api_key: str = Field(..., env="my_api_key")

    redis_dsn: RedisDsn = (
        "redis://user:pass@localhost:6379/1"  # pragma: allowlist secret
    )
    pg_dsn: PostgresDsn = "postgres://user:pass@localhost:5432/foobar"  # pragma: allowlist secret
    amqp_dsn: AmqpDsn = (
        "amqp://user:pass@localhost:5672/"  # pragma: allowlist secret
    )

    special_function: PyObject = "math.cos"

    # to override domains:
    # export my_prefix_domains='["foo.com", "bar.com"]'
    domains: Set[str] = set()

    # to override more_settings:
    # export my_prefix_more_settings='{"foo": "x", "apple": 1}'
    more_settings: SubModel = SubModel()

    class Config:
        env_prefix = "my_prefix_"  # defaults to no prefix, i.e. ""
        fields = {
            "auth_key": {
                "env": "my_auth_key",
            },
            "redis_dsn": {"env": ["service_redis_dsn", "redis_url"]},
        }


print(
    Settings(auth_key="xxx", api_key="zzz").dict()  # pragma: allowlist secret
)
