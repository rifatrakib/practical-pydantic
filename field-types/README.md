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


#### Unions

The `Union` type allows a model attribute to accept different types.

> ##### Info
>
> You may get unexpected coercion with `Union`; see below. Know that you can also make the check slower but stricter by using `Smart Union`.

However, as can be seen above, pydantic will attempt to 'match' any of the types defined under `Union` and will use the first one that matches. In the above example the `id` of `user_3` was defined as a `uuid.UUID` class (which is defined under the attribute's `Union` annotation) but as the `uuid.UUID` can be marshalled into an `int` it chose to match against the `int` type and disregarded the other types.

> ##### Warning
>
> `typing.Union` also ignores order when defined, so `Union[int, float] == Union[float, int]` which can lead to unexpected behaviour when combined with matching based on the Union type order inside other type definitions, such as `List` and `Dict` types (because Python treats these definitions as singletons). For example, `Dict[str, Union[int, float]] == Dict[str, Union[float, int]]` with the order based on the first time it was defined. Please note that this can also be `affected by third party libraries` and their internal type definitions and the import orders.

As such, it is recommended that, when defining `Union` annotations, the most specific type is included first and followed by less specific types. In the above example, the `UUID` class should precede the `int` and `str` classes to preclude the unexpected representation.

> ##### Tip
>
> The type `Optional[x]` is a shorthand for `Union[x, None]`. `Optional[x]` can also be used to specify a required field that can take `None` as a value.


##### Discriminated Unions (a.k.a. Tagged Unions)

When `Union` is used with multiple submodels, you sometimes know exactly which submodel needs to be checked and validated and want to enforce this. To do that you can set the same field - let's call it `my_discriminator` - in each of the submodels with a discriminated value, which is one (or many) `Literal` value(s). For your `Union`, you can set the discriminator in its value: `Field(discriminator='my_discriminator')`.

Setting a discriminated union has many benefits:

* validation is faster since it is only attempted against one model.

* only one explicit error is raised in case of failure.

* the generated JSON schema implements the `associated OpenAPI specification`.

> ##### Note
>
> Using the `Annotated Fields syntax` can be handy to regroup the `Union` and `discriminator` information. See below for an example!

> Warning
>
> Discriminated unions cannot be used with only a single variant, such as `Union[Cat]`. Python changes `Union[T]` into `T` at interpretation time, so it is not possible for pydantic to distinguish fields of `Union[T]` from `T`.


##### Nested Discriminated Unions

Only one discriminator can be set for a field but sometimes you want to combine multiple discriminators. In this case you can always create "intermediate" models with `__root__` and add your discriminator.


#### Enums and Choices

*pydantic* uses Python's standard `enum` classes to define choices.


#### Datetime Types

*Pydantic* supports the following `datetime` types:

* `datetime` fields can be:

  * `datetime`, existing `datetime` object
  * `int` or `float`, assumed as Unix time, i.e. seconds (if >= `-2e10` or <= `2e10`) or milliseconds (if < `-2e10`or > `2e10`) since 1 January 1970
  * `str`, following formats work:

    * `YYYY-MM-DD[T]HH:MM[:SS[.ffffff]][Z or [±]HH[:]MM]]]`
    * `int` or `float` as a string (assumed as Unix time)

* `date` fields can be:

  * `date`, existing `date` object
  * `int` or `float`, see `datetime`
  * `str`, following formats work:

    * `YYYY-MM-DD`
    * `int` or `float`, see `datetime`

* `time` fields can be:

  * `time`, existing `time` object
  * `str`, following formats work:

    * `HH:MM[:SS[.ffffff]][Z or [±]HH[:]MM]]]`

* `timedelta` fields can be:

  * `timedelta`, existing `timedelta` object
  * `int` or `float`, assumed as seconds
  * `str`, following formats work:

    * `[-][DD ][HH:MM]SS[.ffffff]`
    * `[±]P[DD]DT[HH]H[MM]M[SS]S` (ISO 8601)


#### Booleans

> ##### Warning
>
> The logic for parsing `bool` fields has changed as of version **v1.0**. Prior to **v1.0**, `bool` parsing never failed, leading to some unexpected results. The new logic is described below.

A standard `bool` field will raise a `ValidationError` if the value is not one of the following:

* A valid boolean (i.e. `True` or `False`),
* The integers `0` or `1`,
* a `str` which when converted to lower case is one of `"0", "off", "f", "false", "n", "no", "1", "on", "t", "true", "y", "yes"`
* a `bytes` which is valid (per the previous rule) when decoded to `str`

> ##### Note
>
> If you want stricter boolean logic (e.g. a field which only permits `True` and `False`) you can use `StrictBool`.


#### Callable

Fields can also be of type `Callable`.

> ##### Warning
>
> Callable fields only perform a simple check that the argument is callable; no validation of arguments, their types, or the return type is performed.


#### Type

*pydantic* supports the use of `Type[T]` to specify that a field may only accept classes (not instances) that are subclasses of `T`.

You may also use `Type` to specify that any class is allowed.


#### TypeVar

`TypeVar` is supported either unconstrained, constrained or with a bound.


#### Literal Type

> ##### Note
>
> This is a new feature of the Python standard library as of Python 3.8; prior to Python 3.8, it requires the `typing-extensions` package.

_pydantic_ supports the use of `typing.Literal` (or `typing_extensions.Literal` prior to Python 3.8) as a lightweight way to specify that a field may accept only specific literal values.

One benefit of this field type is that it can be used to check for equality with one or more specific values without needing to declare custom validators.

With proper ordering in an annotated `Union`, you can use this to parse types of decreasing specificity.


#### Annotated Types

* `NamedTuple`

* `TypedDict`

> ##### Note
>
> This is a new feature of the Python standard library as of Python 3.8. Prior to Python 3.8, it requires the `typing-extensions` package. But required and optional fields are properly differentiated only since Python 3.9. We therefore recommend using `typing-extensions` with Python 3.8 as well.


#### Pydantic Types

_pydantic_ also provides a variety of other useful types:

* `FilePath`: like `Path`, but the path must exist and be a file.

* `DirectoryPath`: like `Path`, but the path must exist and be a directory.

* `PastDate`: like `date`, but the date should be in the past.

* `FutureDate`: like `date`, but the date should be in the future.

* `EmailStr`: requires `email-validator` to be installed; the input string must be a valid email address, and the output is a simple string.

* `NameEmail`: requires `email-validator` to be installed; the input string must be either a valid email address or in the format `Fred Bloggs <fred.bloggs@example.com>`, and the output is a `NameEmail` object which has two properties: `name` and `email`. For `Fred Bloggs <fred.bloggs@example.com>` the name would be `"Fred Bloggs"`; for `fred.bloggs@example.com` it would be `"fred.bloggs"`.

* `PyObject`: expects a string and loads the Python object importable at that dotted path; e.g. if `'math.cos'` was provided, the resulting field value would be the function `cos`.

* `Color`: for parsing HTML and CSS colors.

* `Json`: a special type wrapper which loads JSON before parsing.

* `PaymentCardNumber`: for parsing and validating payment cards.

* `AnyUrl`: any URL.

* `AnyHttpUrl`: an HTTP URL.

* `HttpUrl`: a stricter HTTP URL.

* `FileUrl`: a file path URL.

* `PostgresDsn`: a postgres DSN style URL.

* `CockroachDsn`: a cockroachdb DSN style URL.

* `RabbitMqDsn`: an `AMQP` DSN style URL as used by RabbitMQ, StormMQ, ActiveMQ etc.

* `RedisDsn`: a redis DSN style URL.

* `MongoDsn`: a MongoDB DSN style URL.

* `KafkaDsn`: a kafka DSN style URL.

* `stricturl`: a type method for arbitrary URL constraints.

* `UUID1`: requires a valid UUID of type 1.

* `UUID3`: requires a valid UUID of type 3.

* `UUID4`: requires a valid UUID of type 4.

* `UUID5`: requires a valid UUID of type 5.

* `SecretBytes`: bytes where the value is kept partially secret.

* `SecretStr`: string where the value is kept partially secret.

* `IPvAnyAddress`: allows either an `IPv4Address` or an `IPv6Address`.

* `IPvAnyInterface`: allows either an `IPv4Interface` or an `IPv6Interface`.

* `IPvAnyNetwork`: allows either an `IPv4Network` or an `IPv6Network`.

* `NegativeFloat`: allows a float which is negative; uses standard `float` parsing then checks the value is less than 0.

* `NegativeInt`: allows a int which is negative; uses standard `int` parsing then checks the value is less than 0.

* `PositiveFloat`: allows a float which is negative; uses standard `float` parsing then checks the value is greater than 0.

* `PositiveInt`: allows a int which is negative; uses standard `int` parsing then checks the value is greater than 0.

* `conbytes`: type method for constraining bytes.

* `condecimal`: type method for constraining Decimals.

* `confloat`: type method for constraining floats.

* `conint`: type method for constraining ints.

* `condate`: type method for constraining dates.

* `conlist`: type method for constraining lists.

* `conset`: type method for constraining sets.

* `confrozenset`: type method for constraining frozen sets.

* `constr`: type method for constraining strs.


#### URLs

For URI/URL validation the following types are available:

* `AnyUrl`: any scheme allowed, TLD not required, host required.

* `AnyHttpUrl`: scheme `http` or `https`, TLD not required, host required.

* `HttpUrl`: scheme `http` or `https`, TLD required, host required, max length 2083.

* `FileUrl`: scheme `file`, host not required.

* `PostgresDsn`: user info required, TLD not required, host required, `PostgresDsn` supports multiple hosts. The following schemes are supported:

    * postgres
    * postgresql
    * postgresql+asyncpg
    * postgresql+pg8000
    * postgresql+psycopg2
    * postgresql+psycopg2cffi
    * postgresql+py-postgresql
    * postgresql+pygresql

* `CockroachDsn`: scheme `cockroachdb`, user info required, TLD not required, host required. Also, its supported DBAPI dialects:

    * cockroachdb+asyncpg
    * cockroachdb+psycopg2

* `AmqpDsn`: schema `amqp` or `amqps`, user info not required, TLD not required, host not required.

* `RedisDsn`: scheme `redis` or `rediss`, user info not required, tld not required, host not required. (CHANGED: user info `rediss://:pass@localhost`)

* `MongoDsn` : scheme `mongodb`, user info not required, database name not required, port not required from __v1.6__ onwards), user info may be passed without user part.

* `stricturl`: method with the following keyword arguments: - `strip_whitespace: bool = True` - `min_length: int = 1` - `max_length: int = 2 ** 16` - `tld_required: bool = True` - `host_required: bool = True` - `allowed_schemes: Optional[Set[str]] = None`.


> ##### Warning
>
> In V1.10.0 and v1.10.1 `stricturl` also took an optional `quote_plus` argument and URL components were percent encoded in some cases.

The above types (which all inherit from `AnyUrl`) will attempt to give descriptive errors when invalid URLs are provided.

If you require a custom URI/URL type, it can be created in a similar way to the types defined above.


##### URL Properties

Assuming an input URL of `http://samuel:pass@example.com:8000/the/path/?query=here#fragment=is;this=bit`, the above types export the following properties: <!-- pragma: allowlist secret -->

* `scheme`: always set - the url scheme (`http` above)

* `host`: always set - the url host (`example.com` above)

* `host_type`: always set - describes the type of host, either:

    * `domain`: e.g. `example.com`,
    * `int_domain`: international domain, e.g. `exampl£e.org`,
    * `ipv4`: an IP V4 address, e.g. `127.0.0.1`, or
    * `ipv6`: an IP V6 address, e.g. `2001:db8:ff00:42`

* `user`: optional - the username if included (`samuel` above)

* `password`: optional - the password if included (`pass` above)

* `tld`: optional - the top level domain (`com` above), __Note: this will be wrong for any two-level domain, e.g. "co.uk"__. You'll need to implement your own list of TLDs if you require full TLD validation

* `port`: optional - the port (`8000` above)

* `path`: optional - the path (`/the/path/` above)

* `query`: optional - the URL query (aka GET arguments or "search string") (`query=here` above)

* `fragment`: optional - the fragment (`fragment=is;this=bit` above)

If further validation is required, these properties can be used by validators to enforce specific behaviour.


##### International Domains

"International domains" (e.g. a URL where the host or TLD includes non-ascii characters) will be encoded via punycode (see this article for a good description of why this is important).

> ##### Underscores in Hostnames
>
> In pydantic underscores are allowed in all parts of a domain except the tld. Technically this might be wrong - in theory the hostname cannot have underscores, but subdomains can.
>
> To explain this; consider the following two cases:
>
> * `exam_ple.co.uk`: the hostname is `exam_ple`, which should not be allowed since it contains an underscore.
> * `foo_bar.example.com`: the hostname is `example`, which should be allowed since the underscore is in the subdomain.
> Without having an exhaustive list of TLDs, it would be impossible to differentiate between these two. Therefore underscores are allowed, but you can always do further validation in a validator if desired.
>
> Also, Chrome, Firefox, and Safari all currently accept `http://exam_ple.com` as a URL, so we're in good (or at least big) company.


#### Color Type

You can use the `Color` data type for storing colors as per `CSS3 specification`. Colors can be defined via:

* name (e.g. `"Black"`, `"azure"`)

* hexadecimal value (e.g. `"0x000"`, `"#FFFFFF"`, `"7fffd4"`)

* RGB/RGBA tuples (e.g. `(255, 255, 255)`, `(255, 255, 255, 0.5)`)

* RGB/RGBA strings (e.g. `"rgb(255, 255, 255)"`, `"rgba(255, 255, 255, 0.5)"`)

* HSL strings (e.g. `"hsl(270, 60%, 70%)"`, `"hsl(270, 60%, 70%, .5)"`)

`Color` has the following methods:

* `original`: the original string or tuple passed to `Color`.

* `as_named`: returns a named CSS3 color; fails if the alpha channel is set or no such color exists unless `fallback=True` is supplied, in which case it falls back to `as_hex`.

* `as_hex`: returns a string in the format `#fff` or `#ffffff`; will contain 4 (or 8) hex values if the alpha channel is set, e.g. `#7f33cc26`.

* `as_rgb`: returns a string in the format `rgb(<red>, <green>, <blue>)`, or `rgba(<red>, <green>, <blue>, <alpha>)` if the alpha channel is set.

* `as_rgb_tuple`: returns a 3- or 4-tuple in RGB(a) format. The `alpha` keyword argument can be used to define whether the alpha channel should be included; options: `True` - always include, `False` - never include, `None` (default) - include if set.

* `as_hsl`: string in the format `hsl(<hue deg>, <saturation %>, <lightness %>)` or `hsl(<hue deg>, <saturation %>, <lightness %>, <alpha>)` if the alpha channel is set.

* `as_hsl_tuple`: returns a 3- or 4-tuple in HSL(a) format. The `alpha` keyword argument can be used to define whether the alpha channel should be included; options: `True` - always include, `False` - never include, `None` (the default) - include if set.

The `__str__` method for `Color` returns `self.as_named(fallback=True)`.

> ##### Note
>
> the `as_hsl*` refer to hue, saturation, lightness "HSL" as used in html and most of the world, __not__ "HLS" as used in Python's `colorsys`.
