## Validation decorator

The `validate_arguments` decorator allows the arguments passed to a function to be parsed and validated using the function's annotations before the function is called. While under the hood this uses the same approach of model creation and initialisation; it provides an extremely easy way to apply validation to your code with minimal boilerplate.


#### Argument Types

Argument types are inferred from type annotations on the function, arguments without a type decorator are considered as `Any`. Since `validate_arguments` internally uses a standard `BaseModel`, all types listed in `types` can be validated, including _pydantic_ models and `custom types`. As with the rest of _pydantic_, types can be coerced by the decorator before they're passed to the actual function.

```
import os
from pathlib import Path
from typing import Pattern, Optional

from pydantic import validate_arguments, DirectoryPath


@validate_arguments
def find_file(path: DirectoryPath, regex: Pattern, max=None) -> Optional[Path]:
    for i, f in enumerate(path.glob('**/*')):
        if max and i > max:
            return
        if f.is_file() and regex.fullmatch(str(f.relative_to(path))):
            return f


# note: this_dir is a string here
this_dir = os.path.dirname(__file__)

print(find_file(this_dir, '^validation.*'))
#> /home/runner/work/pydantic/pydantic/docs/examples/validation_decorator_types.
#> py
print(find_file(this_dir, '^foobar.*', max=3))
#> None
```

A few notes:

* though they're passed as strings, `path` and `regex` are converted to a `Path` object and regex respectively by the decorator

* `max` has no type annotation, so will be considered as `Any` by the decorator

Type coercion like this can be extremely helpful but also confusing or not desired.


#### Function Signatures

The decorator is designed to work with functions using all possible parameter configurations and all possible combinations of these:

* positional or keyword arguments with or without defaults

* variable positional arguments defined via `*` (often `*args`)

* variable keyword arguments defined via `**` (often `**kwargs`)

* keyword only arguments - arguments after `*,`

* positional only arguments - arguments before `, /` (new in Python 3.8)


#### Using Field to describe function arguments

`Field` can also be used with `validate_arguments` to provide extra information about the field and validations. In general it should be used in a type hint with `Annotated`, unless `default_factory` is specified, in which case it should be used as the default value of the field. The `alias` can be used with the decorator as normal.


#### Usage with mypy

The `validate_arguments` decorator should work "out of the box" with `mypy` since it's defined to return a function with the same signature as the function it decorates. The only limitation is that since we trick mypy into thinking the function returned by the decorator is the same as the function being decorated; access to the `raw function` or other attributes will require `type: ignore`.


#### Validate without calling the function

By default, arguments validation is done by directly calling the decorated function with parameters. But what if you wanted to validate them without actually calling the function? To do that you can call the `validate` method bound to the decorated function.


#### Raw function

The raw function which was decorated is accessible, this is useful if in some scenarios you trust your input arguments and want to call the function in the most performant way.


#### Async Functions

`validate_arguments` can also be used on async functions.


#### Custom Config

The model behind `validate_arguments` can be customised using a config setting which is equivalent to setting the `Config` sub-class in normal models.

> The `fields` and `alias_generator` properties of `Config` which allow aliases to be configured are not supported yet with `@validate_arguments`, using them will raise an error.

Configuration is set using the `config` keyword argument to the decorator, it may be either a config class or a dict of properties which are converted to a class later.


#### Limitations

`validate_arguments` has been released on a provisional basis without all the bells and whistles, which may be added late.

* __Validation Exception__: Currently upon validation failure, a standard pydantic `ValidationError` is raised. This is helpful since it's `str()` method provides useful details of the error which occurred and methods like `.errors()` and `.json()` can be useful when exposing the errors to end users, however `ValidationError` inherits from `ValueError` __not__ `TypeError` which may be unexpected since Python would raise a `TypeError` upon invalid or missing arguments. This may be addressed in future by either allow a custom error or raising a different exception by default, or both.

* __Coercion and Strictness__: _pydantic_ currently leans on the side of trying to coerce types rather than raise an error if a type is wrong and `validate_arguments` is no different. If pydantic gets a "strict" mode in future, `validate_arguments` will have an option to use this, it may even become the default for the decorator.

* __Performance__: We've made a big effort to make _pydantic_ as performant as possible and argument inspect and model creation is only performed once when the function is defined, however there will still be a performance impact to using the `validate_arguments` decorator compared to calling the raw function.

In many situations this will have little or no noticeable effect, however be aware that `validate_arguments` is not an equivalent or alternative to function definitions in strongly typed languages; it never will be.

* __Return Value__: The return value of the function is not validated against its return type annotation, this may be added as an option in future.

* __Config and Validators__: `fields` and `alias_generator` on custom Config are not supported, neither are `validators`.

* __Model fields and reserved arguments__: The following names may not be used by arguments since they can be used internally to store information about the function's signature:

    * `v__args`
    * `v__kwargs`
    * `v__positional_only`

These names (together with `"args"` and `"kwargs"`) may or may not (depending on the function's signature) appear as fields on the internal _pydantic_ model accessible via `.model` thus this model isn't especially useful (e.g. for generating a schema) at the moment.

This should be fixable in future as the way error are raised is changed.
