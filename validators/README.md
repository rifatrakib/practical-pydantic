## Validators

Custom validation and complex relationships between objects can be achieved using the `validator` decorator.

```
class UserModel(BaseModel):
    name: str
    username: str
    password1: str
    password2: str

    @validator("name")
    def name_must_contain_space(cls, v):
        if " " not in v:
            raise ValueError("must contain a space")
        return v.title()

    @validator("password2")
    def password_match(cls, v, values, **kwargs):
        if "password1" in values and v != values["password1"]:
            raise ValueError("passwords do not match")
        return v

    @validator("username")
    def username_alphanumeric(cls, v):
        assert v.isalnum(), "must be alphanumeric"
        return v
```

A few things to note on validators:

* validators are "class methods", so the first argument value they receive is the `UserModel` class, not an instance of `UserModel`.

* the second argument is always the field value to validate; it can be named as you please.

* you can also add any subset of the following arguments to the signature (the names __must__ match):

    * `values`: a dict containing the name-to-value mapping of any previously-validated fields.

    * `config`: the model config.

    * `field`: the field being validated. Type of object is `pydantic.fields.ModelField`.

    * `**kwargs`: if provided, this will include the arguments above not explicitly listed in the signature.

* validators should either return the parsed value or raise a `ValueError`, `TypeError`, or `AssertionError` (`assert` statements may be used).

> ##### Warning
>
> If you make use of `assert` statements, keep in mind that running Python with the `-O optimization flag` disables `assert` statements, and __validators will stop working__.

* where validators rely on other values, you should be aware that:

    * Validation is done in the order fields are defined. E.g. in the example above, `password2` has access to `password1` (and `name`), but `password1` does not have access to `password2`. See `Field Ordering` for more information on how fields are ordered.

    * If validation fails on another field (or that field is missing) it will not be included in `values`, hence `if "password1" in values and ...` in this example.
