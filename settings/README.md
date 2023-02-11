## Settings management

One of _pydantic_'s most useful applications is settings management.

If you create a model that inherits from `BaseSettings`, the model initialiser will attempt to determine the values of any fields not passed as keyword arguments by reading from the environment. (Default values will still be used if the matching environment variable is not set.)

This makes it easy to:

* Create a clearly-defined, type-hinted application configuration class

* Automatically read modifications to the configuration from environment variables

* Manually override specific settings in the initialiser where desired (e.g. in unit tests)


#### Environment variable names

The following rules are used to determine which environment variable(s) are read for a given field:

* By default, the environment variable name is built by concatenating the prefix and field name.

    * For example, to override `special_function`, you could use:

    ```
    export my_prefix_special_function="foo.bar"
    ```

    * Note 1: The default prefix is an empty string.

    * Note 2: Field aliases are ignored when building the environment variable name.

* Custom environment variable names can be set in two ways:

    * `Config.fields["field_name"]["env"]` (see `auth_key` and `redis_dsn` in basics)

    * `Field(..., env=...)` (see `api_key` in basics)

* When specifying custom environment variable names, either a string or a list of strings may be provided.

    * When specifying a list of strings, order matters: the first detected value is used.

    * For example, for `redis_dsn` in basics, `service_redis_dsn` would take precedence over `redis_url`.

Case-sensitivity can be turned on through the `Config`.

When `case_sensitive` is `True`, the environment variable names must match field names (optionally with a prefix), so in this example `redis_host` could only be modified via `export redis_host`. If you want to name environment variables all upper-case, you should name attribute all upper-case too. You can still name environment variables anything you like through `Field(..., env=...)`.

In Pydantic __v1__ `case_sensitive` is `False` by default and all variable names are converted to lower-case internally. If you want to define upper-case variable names on nested models like `SubModel` you have to set `case_sensitive=True` to disable this behaviour.


#### Parsing environment variable values

For most simple field types (such as `int`, `float`, `str`, etc.), the environment variable value is parsed the same way it would be if passed directly to the initialiser (as a string).

Complex types like `list`, `set`, `dict`, and sub-models are populated from the environment by treating the environment variable's value as a JSON-encoded string.

Another way to populate nested complex variables is to configure your model with the `env_nested_delimiter` config setting, then use an env variable with a name pointing to the nested module fields. What it does is simply explodes your variable into nested models or dicts. So if you define a variable `FOO__BAR__BAZ=123` it will convert it into `FOO={"BAR": {"BAZ": 123}}` If you have multiple variables with the same structure they will be merged.

`env_nested_delimiter` can be configured via the `Config` class as shown above, or via the `_env_nested_delimiter` keyword argument on instantiation.

JSON is only parsed in top-level fields, if you need to parse JSON in sub-models, you will need to implement validators on those models.

Nested environment variables take precedence over the top-level environment variable JSON (e.g. in the example above, `SUB_MODEL__V2` trumps `SUB_MODEL`).

You may also populate a complex type by providing your own parsing function to the `parse_env_var` classmethod in the Config object.


#### Dotenv (.env) support

Dotenv files (generally named `.env`) are a common pattern that make it easy to use environment variables in a platform-independent manner.

A dotenv file follows the same general principles of all environment variables, and looks something like:

```
# ignore comment
ENVIRONMENT="production"
REDIS_ADDRESS=localhost:6379
MEANING_OF_LIFE=42
MY_VAR='Hello world'
```

Once you have your `.env` file filled with variables, pydantic supports loading it in two ways:

1. setting `env_file` (and `env_file_encoding` if you don't want the default encoding of your OS) on `Config` in a `BaseSettings` class:

```
class Settings(BaseSettings):
    ...

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
```

2. instantiating a `BaseSettings` derived class with the `_env_file` keyword argument (and the `_env_file_encoding` if needed):

```
settings = Settings(_env_file="prod.env", _env_file_encoding="utf-8")
```

In either case, the value of the passed argument can be any valid path or filename, either absolute or relative to the current working directory. From there, pydantic will handle everything for you by loading in your variables and validating them.

Even when using a dotenv file, pydantic will still read environment variables as well as the dotenv file, __environment variables will always take priority over values loaded from a dotenv file__.

Passing a file path via the `_env_file` keyword argument on instantiation (method 2) will override the value (if any) set on the `Config` class. If the above snippets were used in conjunction, `prod.env` would be loaded while `.env` would be ignored.

If you need to load multiple dotenv files, you can pass the file paths as a `list` or `tuple`.

Later files in the list/tuple will take priority over earlier files.

```
from pydantic import BaseSettings

class Settings(BaseSettings):
    ...

    class Config:
        # `.env.prod` takes priority over `.env`
        env_file = ".env", ".env.prod"
```

You can also use the keyword argument override to tell Pydantic not to load any file at all (even if one is set in the `Config` class) by passing `None` as the instantiation keyword argument, e.g. `settings = Settings(_env_file=None)`.

Because python-dotenv is used to parse the file, bash-like semantics such as `export` can be used which (depending on your OS and environment) may allow your dotenv file to also be used with `source`.


#### Secret Support

Placing secret values in files is a common pattern to provide sensitive configuration to an application.

A secret file follows the same principal as a dotenv file except it only contains a single value and the file name is used as the key. A secret file will look like the following:

`/var/run/database_password`

```
super_secret_database_password
```

Once you have your secret files, pydantic supports loading it in two ways:

1. setting `secrets_dir` on `Config` in a `BaseSettings` class to the directory where your secret files are stored:

```
class Settings(BaseSettings):
    ...
    database_password: str

    class Config:
        secrets_dir = "/var/run"
```

2. instantiating a `BaseSettings` derived class with the `_secrets_dir` keyword argument:

```
settings = Settings(_secrets_dir="/var/run")
```

In either case, the value of the passed argument can be any valid directory, either absolute or relative to the current working directory. __Note that a non existent directory will only generate a warning__. From there, pydantic will handle everything for you by loading in your variables and validating them.

Even when using a secrets directory, pydantic will still read environment variables from a dotenv file or the environment, __a dotenv file and environment variables will always take priority over values loaded from the secrets directory__.

Passing a file path via the `_secrets_dir` keyword argument on instantiation (method 2) will override the value (if any) set on the `Config` class.


##### Use Case: Docker Secrets

Docker Secrets can be used to provide sensitive configuration to an application running in a Docker container. To use these secrets in a pydantic application the process is simple. More information regarding creating, managing and using secrets in Docker see the official `Docker documentation`.

First, define your Settings

```
class Settings(BaseSettings):
    my_secret_data: str

    class Config:
        secrets_dir = "/run/secrets"
```

> By default Docker uses `/run/secrets` as the target mount point. If you want to use a different location, change `Config.secrets_dir` accordingly.

Then, create your secret via the Docker CLI

```
printf "This is a secret" | docker secret create my_secret_data -
```

Last, run your application inside a Docker container and supply your newly created secret

```
docker service create --name pydantic-with-secrets --secret my_secret_data pydantic-app:latest
```
