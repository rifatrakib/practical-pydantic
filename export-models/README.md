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
