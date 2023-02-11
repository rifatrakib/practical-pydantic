import json
import os
from pathlib import Path
from typing import Any, Dict, Tuple

from pydantic import BaseSettings, PostgresDsn
from pydantic.env_settings import SettingsSourceCallable


class Settings(BaseSettings):
    database_dsn: PostgresDsn

    class Config:
        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> Tuple[SettingsSourceCallable, ...]:
            return env_settings, init_settings, file_secret_settings


def json_config_settings_source(settings: BaseSettings) -> Dict[str, Any]:
    """A simple settings source that loads variables from a JSON file at the
    project's root.

    Here we happen to choose to use the `env_file_encoding` from Config
    when reading `config.json`
    """
    encoding = settings.__config__.env_file_encoding
    return json.loads(Path("config.json").read_text(encoding))


class CustomSettings(BaseSettings):
    foobar: str

    class Config:
        env_file_encoding = "utf-8"

        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            return (
                init_settings,
                json_config_settings_source,
                env_settings,
                file_secret_settings,
            )


class RemoveSettings(BaseSettings):
    my_api_key: str

    class Config:
        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> Tuple[SettingsSourceCallable, ...]:
            # here we choose to ignore arguments from init_settings
            return env_settings, file_secret_settings


print(Settings(database_dsn="postgres://postgres@localhost:5432/kwargs_db"))
print(CustomSettings())

os.environ["my_api_key"] = "xxx"  # pragma: allowlist secret
print(Settings(my_api_key="this is ignored"))  # pragma: allowlist secret
