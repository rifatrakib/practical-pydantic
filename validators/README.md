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


#### Pre and per-item validators

Validators can do a few more complex things.

```
class DemoModel(BaseModel):
    square_numbers: List[int] = []
    cube_numbers: List[int] = []

    # '*' is the same as 'cube_numbers', 'square_numbers' here:
    @validator("*", pre=True)
    def split_str(cls, v):
        if isinstance(v, str):
            return v.split("|")
        return v

    @validator("cube_numbers", "square_numbers")
    def check_sum(cls, v):
        if sum(v) > 42:
            raise ValueError("sum of numbers greater than 42")
        return v

    @validator("square_numbers", each_item=True)
    def check_squares(cls, v):
        assert v ** 0.5 % 1 == 0, f"{v} is not a square number"
        return v

    @validator("cube_numbers", each_item=True)
    def check_cubes(cls, v):
        # 64 ** (1 / 3) == 3.9999999999999996 (!)
        # this is not a good way of checking cubes
        assert v ** (1 / 3) % 1 == 0, f"{v} is not a cubed number"
        return v
```

A few more things to note:

* a single validator can be applied to multiple fields by passing it multiple field names.

* a single validator can also be called on all fields by passing the special value "*".

* the keyword argument `pre` will cause the validator to be called prior to other validation.

* passing `each_item=True` will result in the validator being applied to individual values (e.g. of `List`, `Dict`, `Set`, etc.), rather than the whole object.
