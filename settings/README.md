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
