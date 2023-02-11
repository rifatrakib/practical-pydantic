## Settings management

One of _pydantic_'s most useful applications is settings management.

If you create a model that inherits from `BaseSettings`, the model initialiser will attempt to determine the values of any fields not passed as keyword arguments by reading from the environment. (Default values will still be used if the matching environment variable is not set.)

This makes it easy to:

* Create a clearly-defined, type-hinted application configuration class

* Automatically read modifications to the configuration from environment variables

* Manually override specific settings in the initialiser where desired (e.g. in unit tests)
