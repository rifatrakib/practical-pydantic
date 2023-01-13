## Dataclasses

If you don't want to use _pydantic_'s `BaseModel` you can instead get the same data validation on standard `dataclasses` (introduced in Python 3.7).

> ##### Note
>
> Keep in mind that `pydantic.dataclasses.dataclass` is a drop-in replacement for `dataclasses.dataclass` with validation, __not a replacement__ for `pydantic.BaseModel` (with a small difference in how `initialization hooks` work). There are cases where subclassing `pydantic.BaseModel` is the better choice.

You can use all the standard _pydantic_ field types, and the resulting dataclass will be identical to the one created by the standard library `dataclass` decorator.

The underlying model and its schema can be accessed through `__pydantic_model__`. Also, fields that require a `default_factory` can be specified by either a `pydantic.Field` or a `dataclasses.field`.

`pydantic.dataclasses.dataclass`'s arguments are the same as the standard decorator, except one extra keyword argument `config` which has the same meaning as `Config`.


#### Dataclass Config

If you want to modify the `Config` like you would with a `BaseModel`, you have three options:

* Option 1 - use directly a dict
  Note: `mypy` will still raise typo error

* Option 2 - use `ConfigDict`
  (same as before at runtime since it's a `TypedDict` but with intellisense)

* Option 3 - use a `Config` class like for a `BaseModel`

> pydantic dataclasses support `Config.extra` but some default behaviour of stdlib dataclasses may prevail. For example, when `print`ing a pydantic dataclass with allowed extra fields, it will still use the `__str__` method of stdlib dataclass and show only the required fields.
