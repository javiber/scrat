# Scrat

Persistent Caching of Expensive Function Results

![🐿️](imgs/scrat.png)

## Get Started

1. Install with `pip install scrat`
2. Initialize stash `scrat init`
3. Start saving time:
``` python
import scrat
import time

@scrat.stash()
def expensive_function(param_1):
    time.sleep(3)
    return param_1

expensive_function(1)  # <- function called
expensive_function(1)  # <- function not called the result is recovered from stash
expensive_function(2)  # <- function called again beacuse the parameters changed
```

## Features

- Seamlessly stores the results of expensive functions to disk for future reuse.
- Automatically re-evaluates the function if the parameters or function code have changed, ensuring up-to-date results.
- Saves any result using the pickle.
- Improved storage of pandas DataFrames.
- Customizable support for alternative serializers.
- Flexible parameter hashing mechanism to efficiently handle any parameter type.
- Command-line interface (CLI) for convenient control and management of the caching functionality.


## Concepts
- `Scrat` is a famous pre-historic squirrel with some bad luck
- `Stash` is composed of a folder where results are saved and a database to index them
- A `Nut` is one of the entries in the database
- The `Squirrel` is in charge of fetching and stashing the `Nuts`
- `Serializer` dumps results to files and load them back to memory
- `Hasher` creates unique hashes for a parameter value
- `HashManager` coordinates hashes of all arguments and functon code

## Development Setup

1. Clone this repo
2. Install [pyenv](https://github.com/pyenv/pyenv#installation).
3. Install the python version used for development running `pyenv install` in the root of this repository.
4. Install [poetry](https://python-poetry.org/docs/#installation). Version `1.5.1` is recommended.
5. Run this command to make sure poetry uses the right python version `poetry env use $(which python)`
6. Install project and dependencies with `poetry install`
7. Run tests with `poetry run pytest` or activate the virtualenv with `poetry shell` and then run `pytest`
