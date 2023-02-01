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
