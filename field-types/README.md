## Field Types

Where possible pydantic uses `standard library types` to define fields, thus smoothing the learning curve. For many useful applications, however, no standard library type exists, so pydantic implements `many commonly used types`.

If no existing type suits your purpose you can also implement your `own pydantic-compatible types` with custom properties and validation.


#### Standard Library Types

pydantic supports many common types from the Python standard library. If you need stricter processing see `Strict Types`; if you need to constrain the values allowed (e.g. to require a positive int) see `Constrained Types`.

* `None`, `type(None)` or `Literal[None]` (equivalent according to `PEP 484`) allows only None value.

* `bool` - see `Booleans` below for details on how bools are validated and what values are permitted.

* `int` - pydantic uses `int(v)` to coerce types to an `int`; see the warning on loss of information during data conversion.

* `float` - similarly, `float(v)` is used to coerce values to floats

* `str` - strings are accepted as-is, `int`, `float`, and `Decimal` are coerced using `str(v)`, `bytes`, and `bytearray` are converted using `v.decode()`, enums inheriting from str are converted using v.value, and all other types cause an error.

* `bytes` - `bytes` are accepted as-is, `bytearray` is converted using `bytes(v)`, `str` are converted using `v.encode()`, and `int`, `float`, and `Decimal` are coerced using `str(v).encode()`.

* `list` - allows `list`, `tuple`, `set`, `frozenset`, `deque`, or generators and casts to a list; see `typing.List` below for sub-type constraints.

* `tuple` - allows `list`, `tuple`, `set`, `frozenset`, `deque`, or generators and casts to a tuple; see `typing.Tuple` below for sub-type constraints.

* `dict` - `dict(v)` is used to attempt to convert a dictionary; see `typing.Dict` below for sub-type constraints.

* `set` - allows `list`, `tuple`, `set`, `frozenset`, `deque`, or generators and casts to a set; see `typing.Set` below for sub-type constraints.

* `frozenset` - allows `list`, `tuple`, `set`, `frozenset`, `deque`, or generators and casts to a frozen set; see `typing.FrozenSet` below for sub-type constraints.

* `deque` - allows `list`, `tuple`, `set`, `frozenset`, `deque`, or generators and casts to a deque; see `typing.Deque` below for sub-type constraints.

* `datetime.date` - see `Datetime Types` below for more detail on parsing and validation.

* `datetime.time` - see `Datetime Types` below for more detail on parsing and validation.

* `datetime.datetime` - see `Datetime Types` below for more detail on parsing and validation.

* `datetime.timedelta` - see `Datetime Types` below for more detail on parsing and validation.

* `typing.Any` - allows any value including `None`, thus an `Any` field is optional.

* `typing.Annotated` - allows wrapping another type with arbitrary metadata, as per `PEP-593`. The `Annotated` hint may contain a single call to the `Field function`, but otherwise the additional metadata is ignored and the root type is used.

* `typing.TypeVar` - constrains the values allowed based on `constraints` or `bound`, see `TypeVar`.

* `typing.Union` - see `Unions` below for more detail on parsing and validation.

* `typing.Optional` - `Optional[x]` is simply short hand for `Union[x, None]`; see `Unions` below for more detail on parsing and validation and `Required Fields` for details about required fields that can receive `None` as a value.

* `typing.List` - see `Typing Iterables` below for more detail on parsing and validation.

* `typing.Tuple` - see `Typing Iterables` below for more detail on parsing and validation.

* subclass of `typing.NamedTuple` - Same as `tuple` but instantiates with the given namedtuple and validates fields since they are annotated. See `Annotated Types` below for more detail on parsing and validation.

* subclass of `collections.namedtuple` - Same as subclass of `typing.NamedTuple` but all fields will have type `Any` since they are not annotated.

* `typing.Dict` - see `Typing Iterables` below for more detail on parsing and validation.

* subclass of `typing.TypedDict` - Same as `dict` but pydantic will validate the dictionary since keys are annotated. See `Annotated Types` below for more detail on parsing and validation.

* `typing.Set` - see `Typing Iterables` below for more detail on parsing and validation.

* `typing.FrozenSet` - see `Typing Iterables` below for more detail on parsing and validation.

* `typing.Deque` - see `Typing Iterables` below for more detail on parsing and validation.

* `typing.Sequence` - see `Typing Iterables` below for more detail on parsing and validation.

* `typing.Iterable` - this is reserved for iterables that shouldn't be consumed. See `Infinite Generators` below for more detail on parsing and validation.

* `typing.Type` - see `Type` below for more detail on parsing and validation.

* `typing.Callable` - see `Callable` below for more detail on parsing and validation.

* `typing.Pattern` - will cause the input value to be passed to `re.compile(v)` to create a regex pattern.

* `ipaddress.IPv4Address` - simply uses the type itself for validation by passing the value to `IPv4Address(v)`; see `Pydantic Types` for other custom IP address types.

* `ipaddress.IPv4Interface` - simply uses the type itself for validation by passing the value to `IPv4Interface(v)`; see `Pydantic Types` for other custom IP address types.

* `ipaddress.IPv4Network` - simply uses the type itself for validation by passing the value to `IPv4Network(v)`; see `Pydantic Types` for other custom IP address types.

* `ipaddress.IPv6Address` - simply uses the type itself for validation by passing the value to `IPv6Address(v)`; see `Pydantic Types` for other custom IP address types.

* `ipaddress.IPv6Interface` - simply uses the type itself for validation by passing the value to `IPv6Interface(v)`; see `Pydantic Types` for other custom IP address types.

* `ipaddress.IPv6Network` - simply uses the type itself for validation by passing the value to `IPv6Network(v)`; see `Pydantic Types` for other custom IP address types.

* `enum.Enum` - checks that the value is a valid Enum instance.

* subclass of `enum.Enum` - checks that the value is a valid member of the enum; see `Enums and Choices` for more details.

* `enum.IntEnum` - checks that the value is a valid IntEnum instance.

* subclass of `enum.IntEnum` - checks that the value is a valid member of the integer enum; see `Enums and Choices` for more details.

* `decimal.Decimal` - pydantic attempts to convert the value to a string, then passes the string to `Decimal(v)`.

* `pathlib.Path` - simply uses the type itself for validation by passing the value to `Path(v)`; see `Pydantic Types` for other more strict path types.

* `uuid.UUID` - strings and bytes (converted to strings) are passed to `UUID(v)`, with a fallback to `UUID(bytes=v)` for `bytes` and `bytearray`; see `Pydantic Types` for other stricter UUID types.

* `ByteSize` - converts a bytes string with units to bytes.


#### Typing Iterables

_pydantic_ uses standard library `typing` types as defined in PEP 484 to define complex objects.


#### Infinite Generators

If you have a generator you can use `Sequence` as described above. In that case, the generator will be consumed and stored on the model as a list and its values will be validated with the sub-type of `Sequence` (e.g. `int` in `Sequence[int]`).

But if you have a generator that you don't want to be consumed, e.g. an infinite generator or a remote data loader, you can define its type with `Iterable`.

> ##### Warning
>
> `Iterable` fields only perform a simple check that the argument is iterable and won't be consumed. No validation of their values is performed as it cannot be done without consuming the iterable.

> Tip
>
> If you want to validate the values of an infinite generator you can create a separate model and use it while consuming the generator, reporting the validation errors as appropriate. pydantic can't validate the values automatically for you because it would require consuming the infinite generator.


##### Validating the first value

You can create a `validator` to validate the first value in an infinite generator and still not consume it entirely.
