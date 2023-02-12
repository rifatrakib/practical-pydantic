#### Postponed annotations

> Both postponed annotations via the future import and `ForwardRef` require Python 3.7+.

Postponed annotations (as described in `PEP563`) "just work".

Internally, pydantic will call a method similar to `typing.get_type_hints` to resolve annotations.

In cases where the referenced type is not yet defined, `ForwardRef` can be used (although referencing the type directly or by its string is a simpler solution in the case of `self-referencing models`).

In some cases, a `ForwardRef` won't be able to be resolved during model creation. For example, this happens whenever a model references itself as a field type. When this happens, you'll need to call `update_forward_refs` after the model has been created before it can be used.

> To resolve strings (type names) into annotations (types), pydantic needs a namespace dict in which to perform the lookup. For this it uses `module.__dict__`, just like `get_type_hints`. This means pydantic may not play well with types not defined in the global scope of a module.


#### Self-referencing Models

Data structures with self-referencing models are also supported. Self-referencing fields will be automatically resolved after model creation.

Within the model, you can refer to the not-yet-constructed model using a string.

Since Python 3.7, you can also refer it by its type, provided you import `annotations` (see above for support depending on Python and pydantic versions).
