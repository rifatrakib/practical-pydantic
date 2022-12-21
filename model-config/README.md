## Model Config

Behaviour of _pydantic_ can be controlled via the `Config` class on a model or a _pydantic_ dataclass. Also, you can specify config options as model class kwargs. Similarly, if using the `@dataclass` decorator.


#### Options

* `title`: the title for the generated JSON Schema

* `anystr_strip_whitespace`: whether to strip leading and trailing whitespace for str & byte types (default: `False`)

* `anystr_upper`: whether to make all characters uppercase for str & byte types (default: `False`)

* `anystr_lower`: whether to make all characters lowercase for str & byte types (default: `False`)

* `min_anystr_length`: the min length for str & byte types (default: `0`)

* `max_anystr_length`: the max length for str & byte types (default: `None`)

* `validate_all`: whether to validate field defaults (default: `False`)

* `extra`: whether to ignore, allow, or forbid extra attributes during model initialization. Accepts the string values of `'ignore'`, `'allow'`, or `'forbid'`, or values of the `Extra` enum (default: `Extra.ignore`). `'forbid'` will cause validation to fail if extra attributes are included, `'ignore'` will silently ignore any extra attributes, and `'allow'` will assign the attributes to the model

* `allow_mutation`: whether or not models are faux-immutable, i.e. whether `__setattr__` is allowed (default: `True`)

* `frozen`: setting `frozen=True` does everything that `allow_mutation=False` does, and also generates a `__hash__()` method for the model. This makes instances of the model potentially hashable if all the attributes are hashable. (default: `False`)

* `use_enum_values`: whether to populate models with the `value` property of enums, rather than the raw enum. This may be useful if you want to serialise `model.dict()` later (default: `False`)

* `fields`: a `dict` containing schema information for each field; this is equivalent to using the `Field` class, except when a field is already defined trough annotation or the Field class, in which case only `alias`, `include`, `exclude`, `min_length`, `max_length`, `regex`, `gt`, `lt`, `gt`, `le`, `multiple_of`, `max_digits`, `decimal_places`, `min_items`, `max_items`, `unique_items` and allow_mutation can be set (for example you cannot set default of default_factory) (default: `None`)

* `validate_assignment`: whether to perform validation on assignment to attributes (default: `False`)

* `allow_population_by_field_name`: whether an aliased field may be populated by its name as given by the model attribute, as well as the alias (default: `False`)

* `error_msg_templates`: a `dict` used to override the default error message templates. Pass in a dictionary with keys matching the error messages you want to override (default: `{}`)

* `arbitrary_types_allowed`: whether to allow arbitrary user types for fields (they are validated simply by checking if the value is an instance of the type). If `False`, `RuntimeError` will be raised on model declaration (default: `False`)

* `orm_mode`: whether to allow usage of ORM mode

* `getter_dict`: a custom class (which should inherit from `GetterDict`) to use when decomposing arbitrary classes for validation, for use with `orm_mode`

* `alias_generator`: a callable that takes a field name and returns an alias for it

* `keep_untouched`: a tuple of types (e.g. descriptors) for a model's default values that should not be changed during model creation and will not be included in the model schemas. __Note__: this means that attributes on the model with defaults of this type, not annotations of this type, will be left alone

* `schema_extra`: a `dict` used to extend/update the generated JSON Schema, or a callable to post-process it

* `json_loads`: a custom function for decoding JSON

* `json_dumps`: a custom function for encoding JSON

* `json_encoders`: a `dict` used to customise the way types are encoded to JSON

* `underscore_attrs_are_private`: whether to treat any underscore non-class var attrs as private, or leave them as is

* `copy_on_model_validation`: string literal to control how models instances are processed during validation, with the following means:

    * `"none"`: models are not copied on validation, they're simply kept "untouched"
    * `"shallow"`: models are shallow copied, this is the default
    * `"deep"`: models are deep copied

* `smart_union`: whether pydantic should try to check all types inside `Union` to prevent undesired coercion

* `post_init_call`: whether stdlib dataclasses `__post_init__` should be run before (default behaviour with value `'before_validation'`) or after (value `'after_validation'`) parsing and validation when they are converted

* `allow_inf_nan`: whether to allows infinity (`+inf` an `-inf`) and NaN values to float fields, defaults to `True`, set to `False` for compatibility with `JSON`


#### Change behaviour globally

If you wish to change the behaviour of pydantic globally, you can create your own custom `BaseModel` with custom `Config` since the config is inherited.
