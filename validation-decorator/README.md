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
