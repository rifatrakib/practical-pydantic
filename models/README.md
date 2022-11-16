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
