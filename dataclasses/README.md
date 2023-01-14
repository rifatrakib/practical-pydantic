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


#### Nested dataclasses

Nested dataclasses are supported both in dataclasses and normal models. Dataclasses attributes can be populated by tuples, dictionaries or instances of the dataclass itself.


#### Stdlib dataclasses and pydantic dataclasses


##### Convert stdlib dataclasses into pydantic dataclasses

Stdlib dataclasses (nested or not) can be easily converted into pydantic dataclasses by just decorating them with `pydantic.dataclasses.dataclass`. Pydantic will enhance the given stdlib dataclass but won't alter the default behaviour (i.e. without validation). It will instead create a wrapper around it to trigger validation that will act like a plain proxy. The stdlib dataclass can still be accessed via the `__dataclass__` attribute.


##### Choose when to trigger validation

As soon as your stdlib dataclass has been decorated with pydantic dataclass decorator, magic methods have been added to validate input data. If you want, you can still keep using your dataclass and choose when to trigger it.


##### Inherit from stdlib dataclasses

Stdlib dataclasses (nested or not) can also be inherited and pydantic will automatically validate all the inherited fields.


##### Use of stdlib dataclasses with `BaseModel`

Bear in mind that stdlib dataclasses (nested or not) are __automatically converted__ into pydantic dataclasses when mixed with `BaseModel`! Furthermore the generated pydantic dataclass will have the __exact same configuration__ (`order`, `frozen`, ...) as the original one.


##### Use custom types

Since stdlib dataclasses are automatically converted to add validation using custom types may cause some unexpected behaviour. In this case you can simply add `arbitrary_types_allowed` in the config!
