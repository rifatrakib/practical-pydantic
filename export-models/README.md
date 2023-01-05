## Exporting models

As well as accessing model attributes directly via their names (e.g. `model.foobar`), models can be converted and exported in a number of ways.


#### `model.dict(...)`

This is the primary way of converting a model to a dictionary. Sub-models will be recursively converted to dictionaries.

Arguments:

* `include`: fields to include in the returned dictionary

* `exclude`: fields to exclude from the returned dictionary

* `by_alias`: whether field aliases should be used as keys in the returned dictionary; default `False`

* `exclude_unset`: whether fields which were not explicitly set when creating the model should be excluded from the returned dictionary; default `False`

* `exclude_defaults`: whether fields which are equal to their default values (whether set or otherwise) should be excluded from the returned dictionary; default `False`

* `exclude_none`: whether fields which are equal to `None` should be excluded from the returned dictionary; default `False`


#### `dict(model)` and iteration

_pydantic_ models can also be converted to dictionaries using `dict(model)`, and you can also iterate over a model's field using `for field_name, value in model:`. With this approach the raw field values are returned, so sub-models will not be converted to dictionaries.


#### `model.copy(...)`

`copy()` allows models to be duplicated, which is particularly useful for immutable models.

Arguments:

* `include`: fields to include in the returned dictionary

* `exclude`: fields to exclude from the returned dictionary

* `update`: a dictionary of values to change when creating the copied model

* `deep`: whether to make a deep copy of the new model; default `False`


#### `model.json(...)`

The `.json()` method will serialise a model to JSON. (For models with a `custom root type`, only the value for the `__root__` key is serialised)

Arguments:

* `include`: fields to include in the returned dictionary; see below

* `exclude`: fields to exclude from the returned dictionary; see below

* `by_alias`: whether field aliases should be used as keys in the returned dictionary; default `False`

* `exclude_unset`: whether fields which were not set when creating the model and have their
default values should be excluded from the returned dictionary; default `False`

* `exclude_defaults`: whether fields which are equal to their default values (whether set or otherwise) should be excluded from the returned dictionary; default `False`

* `exclude_none`: whether fields which are equal to `None` should be excluded from the returned dictionary; default `False`

* encoder: a custom encoder function passed to the `default` argument of `json.dumps()`; defaults to a custom encoder designed to take care of all common types

* `**dumps_kwargs`: any other keyword arguments are passed to `json.dumps()`, e.g. `indent`.

_pydantic_ can serialise many commonly used types to JSON (e.g. `datetime`, `date` or `UUID`) which would normally fail with a simple `json.dumps(foobar)`.


##### `json_encoders`

Serialisation can be customised on a model using the `json_encoders` config property; the keys should be types (or names of types for forward references), and the values should be functions which serialise that type.

By default, `timedelta` is encoded as a simple float of total seconds. The `timedelta_isoformat` is provided as an optional alternative which implements `ISO 8601` time diff encoding.

The `json_encoders` are also merged during the models inheritance with the child encoders taking precedence over the parent one.


##### Serialising self-reference or other models

By default, models are serialised as dictionaries. If you want to serialise them differently, you can add `models_as_dict=False` when calling `json()` method and add the classes of the model in `json_encoders`. In case of forward references, you can use a string with the class name instead of the class itself.


##### Serialising subclasses

Subclasses of common types are automatically encoded like their super-classes.


##### Custom JSON (de)serialisation

To improve the performance of encoding and decoding JSON, alternative JSON implementations (e.g. `ujson`) can be used via the `json_loads` and `json_dumps` properties of `Config`.

`ujson` generally cannot be used to dump JSON since it doesn't support encoding of objects like datetimes and does not accept a `default` fallback function argument. To do this, you may use another library like `orjson`.

Note that `orjson` takes care of `datetime` encoding natively, making it faster than `json.dumps` but meaning you cannot always customise the encoding using `Config.json_encoders`.
