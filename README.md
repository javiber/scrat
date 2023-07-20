# 🐿️ Scrat

Easily stash the results of expensive functions to disk.

## Get Started

1. Install with `pip install git+https://github.com/javiber/scrat.git` (pypi package coming soon)
2. Initialize stash `scrat init`
3. Start saving time:
``` python
import scrat as sc
import time

@sc.stash()
def expensive_function(param_1):
    time.sleep(3)
    return param_1

expensive_function(1)  # <- function called
expensive_function(1)  # <- function not called the result is recovered from stash
expensive_function(2)  # <- function called again beacuse the parameters changed
```

## Features

- Stores results to disk so they can be reused in different runs
- Automatically re-runs the function if the parameters or the function code changed
- Automatically saves any result using pickle
- Automatically saves pandas DataFrames as parquet
- Customizable to allow other serializers to store any kind of result efficiently
- Customizable to hash any type of parameter efficiently
- CLI to control stash


## Concepts
- `Scrat` is a famous pre-historic squirrel with some bad luck
- `Stash` is composed of a folder where results are saved and a database to index them
- A `Nut` is one of the entries in the database
- The `Squirrel` is in charge of fetching and stashing the nuts
- `Serializer` dumps results to files and load them back to memory
- `Hasher` creates unique hashes for a parameter value
- `HashManager` coordinates hashes of all arguments and functon code