## Models

The primary means of defining objects in pydantic is via models (models are simply classes which inherit from `BaseModel`).

You can think of models as similar to types in strictly typed languages, or as the requirements of a single endpoint in an API.

Untrusted data can be passed to a model, and after parsing and validation pydantic guarantees that the fields of the resultant model instance will conform to the field types defined on the model.

> ##### Note
>
> pydantic is primarily a parsing library, not a validation library. Validation is a means to an end: building a model which conforms to the types and constraints provided.
>
> In other words, pydantic guarantees the types and constraints of the output model, not the input data.
>
> This might sound like an esoteric distinction, but it is not. If you're unsure what this means or how it might affect your usage you should read the section about `Data Conversion` below.
>
> Although validation is not the main purpose of pydantic, you can use this library for custom `validation`.


#### Basic model usage

```
class User(BaseModel):
    id: int
    name = "Jane Doe"
```

`User` here is a model with two fields `id` which is an integer and is required, and `name` which is a string and is not required (it has a default value). The type of `name` is inferred from the default value, and so a type annotation is not required.

```
user = User(id="123")
user_x = User(id=123.45)
```

`user` here is an instance of `User`. Initialisation of the object will perform all parsing and validation, if no `ValidationError` is raised, you know the resulting model instance is valid.

More details on the casting in the case of `user_x` can be found in `Data Conversion`. Fields of a model can be accessed as normal attributes of the user object. The string "123" has been cast to an int as per the field type

```
assert user.name == "Jane Doe"
```

`name` wasn't set when user was initialised, so it has the default value. The fields which were supplied when user was initialised can be found with

```
assert user.__fields_set__ == {"id"}
```

Either `.dict()` or `dict(user)` will provide a dict of fields, but `.dict()` can take numerous other arguments. This model is mutable so field values can be changed.


##### Model properties

The example above only shows the tip of the iceberg of what models can do. Models possess the following methods and attributes:

* `dict()`: returns a dictionary of the model's fields and values; cf. `exporting models`

* `json()`: returns a JSON string representation dict(); cf. `exporting models`

* `copy()`: returns a copy (by default, shallow copy) of the model; cf. `exporting models`

* `parse_obj()`: a utility for loading any object into a model with error handling if the object is not a dictionary; cf. `helper functions`

* `parse_raw()`: a utility for loading strings of numerous formats; cf. `helper functions`

* `parse_file()`: like parse_raw() but for file paths; cf. `helper functions`

* `from_orm()`: loads data into a model from an arbitrary class; cf. `ORM mode`

* `schema()`: returns a dictionary representing the model as JSON Schema; cf. `schema`

* `schema_json()`: returns a JSON string representation of schema(); cf. `schema`

* `construct()`: a class method for creating models without running validation; cf. `Creating models without validation`

* `__fields_set__`: Set of names of fields which were set when the model instance was initialised

* `__fields__`: a dictionary of the model's fields

* `__config__`: the configuration class for the model, cf. `model config`


#### Recursive Models

More complex hierarchical data structures can be defined using models themselves as types in annotations. For self-referencing models, see `postponed annotations`.


#### ORM Mode (aka Arbitrary Class Instances)

Pydantic models can be created from arbitrary class instances to support models that map to ORM objects. To do this:

1. The `Config` property `orm_mode` must be set to `True`.

2. The special constructor `from_orm` must be used to create the model instance.

The example here uses `SQLAlchemy`, but the same approach should work for any ORM.

```
class CompanyOrm(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True, nullable=False)
    public_key = Column(String(20), index=True, nullable=False, unique=True)
    name = Column(String(63), unique=True)
    domains = Column(ARRAY(String(255)))


class CompanyModel(BaseModel):
    id: int
    public_key: constr(max_length=20)
    name: constr(max_length=63)
    domains: List[constr(max_length=255)]

    class Config:
        orm_mode = True
```


##### Reserved names

You may want to name a Column after a reserved SQLAlchemy field. In that case, Field aliases will be convenient.

```
class MyModel(BaseModel):
    metadata: Dict[str, str] = Field(alias="metadata_")

    class Config:
        orm_mode = True


class SQLModel(Base):
    __tablename__ = "my_table"
    id = Column("id", Integer, primary_key=True)
    metadata_ = Column("metadata", JSON)
```

> ##### Note
>
> The example above works because aliases have priority over field names for field population. Accessing `SQLModel`'s `metadata` attribute would lead to a `ValidationError`.


##### Recursive ORM models

ORM instances will be parsed with `from_orm` recursively as well as at the top level. Here a vanilla class is used to demonstrate the principle, but any ORM class could be used instead.

```
class PetCls:
    def __init__(self, *, name: str, species: str):
        self.name = name
        self.species = species


class PersonCls:
    def __init__(self, *, name: str, age: float = None, pets: List[PetCls]):
        self.name = name
        self.age = age
        self.pets = pets


class Pet(BaseModel):
    name: str
    species: str

    class Config:
        orm_mode = True


class Person(BaseModel):
    name: str
    age: float = None
    pets: List[Pet]

    class Config:
        orm_mode = True
```


##### Data binding

Arbitrary classes are processed by pydantic using the `GetterDict` class, which attempts to provide a dictionary-like interface to any class. You can customise how this works by setting your own sub-class of `GetterDict` as the value of `Config.getter_dict` (see `config`).

You can also customise class validation using `root_validators` with `pre=True`. In this case your validator function will be passed a `GetterDict` instance which you may copy and modify.

The `GetterDict` instance will be called for each field with a sentinel as a fallback (if no other default value is set). Returning this sentinel means that the field is missing. Any other value will be interpreted as the value of the field.


#### Error Handling

pydantic will raise `ValidationError` whenever it finds an error in the data it's validating.

> ##### Note
>
> Validation code should not raise `ValidationError` itself, but rather raise `ValueError`, `TypeError` or `AssertionError` (or subclasses of `ValueError` or `TypeError`) which will be caught and used to populate `ValidationError`.

One exception will be raised regardless of the number of errors found, that `ValidationError` will contain information about all the errors and how they happened. You can access these errors in several ways:

* `e.errors()`: method will return list of errors found in the input data.

* `e.json()`: method will return a JSON representation of `errors`.

* `str(e)`: method will return a human readable representation of the errors.

Each error object contains:

* `loc`: the error's location as a list. The first item in the list will be the field where the error occurred, and if the field is a `sub-model`, subsequent items will be present to indicate the nested location of the error.

* `type`: a computer-readable identifier of the error type.

* `msg`: a human readable explanation of the error.

* `ctx`: an optional object which contains values required to render the error message.


##### Custom Errors

In your custom data types or validators you should use `ValueError`, `TypeError` or `AssertionError` to raise errors.

See `validators` for more details on use of the `@validator` decorator.

You can also define your own error classes, which can specify a custom error code, message template, and context.
