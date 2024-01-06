# Gatting Started

## Installation and Setup

### From pypi

Simply run `pip install scrat`

### From Github

To install the latest version from github run `pip install git+https://github.com/javiber/scrat.git@main#egg=scrat`

### Setup

Before using scrat you need to initialize the cache first by running `scrat init`.
This will create a folder `.scrat` in the current directory which contains the `stash` folder where the results are saved and a sqlite file (`stash.db`) where we index the results.

## Basic Usage

The most basic use-case is to cache the results of slow functions, let's create a slow function and call it from a python script:

```python
# sample.py
import time

import scrat as sc


@sc.stash()
def slow_square(a):
    time.sleep(1)
    return a**2


if __name__ == "__main__":
    a = 2
    t0 = time.time()
    result = slow_square(a)
    t1 = time.time()
    print(f"Function took {t1-t0:.1f}s, the square of {a} is {result}")
```

Now we call the script from the console:

```bash
> python sample.py
Function took 1.0s, the square of 2 is 4

> python sample.py
Function took 0.0s, the square of 2 is 4

> scrat stash list
name        hash                             created_at       size
slow_square 724c8df5b6e9961d194ee0e24e385d44 2023-08-08 15:29 5.0B
```

> Notice that the second time we called the scrip, the result is recovered from the stash saving us the 1 second execution time.

Next, change the parameter `a` to `4` in line `13` and call the script again.

```bash
> python sample.py
Function took 1.0s, the square of 4 is 16

> scrat stash list
name        hash                             created_at       size
slow_square 724c8df5b6e9961d194ee0e24e385d44 2023-08-08 15:29 5.0B
slow_square 589e5491ea30ed09f40e117078a302ef 2023-08-08 15:30 5.0B
```

> Since we changed the parameters, the function is called again and a new entry is added to the stash.

Finally, change the function's code in line `9` to make it return the cube of `a`, `a**3` and call the script one more time:

```bash
> python sample.py
Function took 1.0s, the square of 4 is 64

> scrat stash list
name        hash                             created_at       size
slow_square 724c8df5b6e9961d194ee0e24e385d44 2023-08-08 15:29 5.0B
slow_square 589e5491ea30ed09f40e117078a302ef 2023-08-08 15:30 5.0B
slow_square e74a0c542fab2c6280e21d48a4fc916d 2023-08-08 15:32 5.0B
```

> Scrat notices that the function code has changed so it calls it again.

Scrat is ideal to store the results of any **deterministic** and **expensive** function such as complex calculations or queries.

## Serializer

### Specifying a built-in serializer

By default Scrat will use pickle to store the results in disk as it can handle a wide variety of objects, however, there are better alternatives if you know the result's type.

For instance, you can easily switch to using json by specifying the serializer like this:

```python
# json_serializer.py
import scrat as sc


@sc.stash(serializer=sc.JsonSerializer())
def get_results():
    print("function called")
    return [{"result": 1}, {"result": 2}]


if __name__ == "__main__":
    print(get_results())
```

Now let's run the script

```bash
> python json_serializer.py
function called
[{'result': 1}, {'result': 2}]
> python json_serializer.py
[{'result': 1}, {'result': 2}]
> scrat stash list
name        hash                             created_at       size
get_results cdd21f31ae5589a465175765f0fb545d 2023-08-14 23:16 30.0B
> cat .scrat/stash/get_results_cdd21f31ae5589a465175765f0fb545d
[{"result": 1}, {"result": 2}]
```

You can find the list of built-in serializers [here](reference/serializer.md)

### Specifying the Return Type

Scrat will also choose a better serializer if you indicate the return type of your function, For instance:

```python
# numpy_serializer.py
import numpy as np
import scrat as sc

@sc.stash()
def np_func(size) -> np.ndarray:
    print("function called")
    return np.eye(size)

if __name__ == "__main__":
    print(np_func(3))
```

> By adding the typehint, Scrat will automatically use the [NumpySerializer][scrat.serializer.NumpySerializer] which relies on the `numpy.save` and `numpy.load` methods.

### Custom Serializer

We are working on adding more serializers (pull requests are welcome 😉), in the meantime, we made sure that adding a custom Serializer can be done by implementing a simple interface:

```python
# custom_serializer.py
from pathlib import Path

import torch

import scrat as sc


class TorchSerializer(sc.Serializer):
    def load(self, path: Path) -> torch.Tensor:
        return torch.load(path)

    def dump(self, obj: torch.Tensor, path: Path):
        torch.save(obj, path)


@sc.stash(serializer=TorchSerializer())
def func():
    print("Function called")
    return torch.ones((3, 3))


if __name__ == "__main__":
    print(func())
```

```bash
> python custom_serializer.py
Function called
tensor([[1., 1., 1.],
        [1., 1., 1.],
        [1., 1., 1.]])
> python custom_serializer.py
tensor([[1., 1., 1.],
        [1., 1., 1.],
        [1., 1., 1.]])
> scrat stash list
name       hash                             created_at       size
func       2f7059606083e1f5a1390a16900fce3a 2023-08-14 23:31 965.0B
```

## Hashing

Hashing is a very important concept, each time you invoke a stashed function a hash is calculated
and used to search for a stored result. By default, the hash includes the arguments and the function's code so you always get the correct behavior if your function meets this 3 conditions:

- deterministic (i.e. the output is not random or random seeds are fixed)
- doesn't access global variables that could change
- doesn't call another functions that could change

The first point is self-explanatory, Scrat can't guess if the result of a random function is going to change or not but the other 2 points are worth discussing further.

### Global Variables

Here is a function that access a global variable:

```python
# global_var.py
import scrat as sc

GLOBAL_VAR = 2


@sc.stash()
def sum_global(a=1):
    print("Function called")
    return a + GLOBAL_VAR


if __name__ == "__main__":
    a = 1
    # The First call gets the correct result
    print(f"{a}+{GLOBAL_VAR}={sum_global(1)}")

    GLOBAL_VAR = 3
    # The function and the parameters have not changed so Scrat will return the old
    # value of 3.
    # This happens because GLOBAL_VAR is not being considered in the hash
    print(f"{a}+{GLOBAL_VAR}={sum_global(1)}")

```

Luckely, this is easily fixable by adding a watched global variable:

```python
# global_car_fixed.py
import scrat as sc

GLOBAL_VAR = 2


@sc.stash(watch_globals=["GLOBAL_VAR"])
def sum_global(a=1):
    print("Function called")
    return a + GLOBAL_VAR


if __name__ == "__main__":
    a = 1
    # The First call gets the correct result
    print(f"{a}+{GLOBAL_VAR}={sum_global(1)}")

    GLOBAL_VAR = 3
    # And the second one does too
    print(f"{a}+{GLOBAL_VAR}={sum_global(1)}")
```

Now the behavior is corrected:

```bash
> python global_var_fixed.py
Function called
1+2=3
Function called
1+3=4
```

### Nested Functions

Similarly if your function calls another function which code changed, Scrat is not going to notice and it will return the old result but, again, this is easily fixable by adding a watched function:

```python
# nested_function.py
import scrat as sc


def nested_func():
    return 2


@sc.stash(watch_functions=[nested_func])
def func(a=1):
    print("Function called")
    return a + nested_func()


if __name__ == "__main__":
    print(func(1))
```

> Now if you ever change the result of nested_func, the function is going to be re-run.

### Ignore Arguments

By default, Scrat assumes that all the arguments affect the result which might not allways be true.
For instance some arguments might only affect the logging and thus should not be included in the hash this can be controlled using the `ignore_args`:

```python
# ignore_argmuents.py
import scrat as sc

@sc.stash(ignore_args=["verbose"])
def double(a, verbose):
    if verbose:
        print(f"Function called with verbose={verbose}")
    else:
        print("Function called")
    return a * 2


if __name__ == "__main__":
    print(double(1, verbose=True))
    print(double(1, verbose=False))
```

### Force Hasher

Scrat tries to use a sane hasher according to the type of each argument, unfurtunatelly, this can fail. We are working on making this process more robust but in the meantime, if you encounter any issue you can control which hasher is used
for each argument:

```python
# force_hasher.py
import numpy as np

import scrat as sc


@sc.stash(hashers={"a": sc.NumpyHasher()})
def double(a):
    return a * 2


if __name__ == "__main__":
    print(double(np.arange(10)))
```

This is useful if you want to change the default parameters of some of the hashers, for more info about the available hashers, check this [doc][scrat.hasher].

### Custom Hasher

Adding a custom hasher is easy, you just need to implement a simple interface and tell scrat which parameters should use it:

```python
# custom_hasher.py
import torch

import scrat as sc


class TorchHasher(sc.hasher.Hasher):
    def hash(self, value: torch.Tensor) -> str:
        return self.md5_hash(value.numpy())


@sc.stash(hashers={"a": TorchHasher()})
def double(a):
    return a * 2


if __name__ == "__main__":
    print(double(torch.arange(10)))
```

The class [Hasher][scrat.hasher.Hasher] provides the method [md5_hash][scrat.hasher.Hasher.md5_hash] that turns any string of buffer into an md5 digest, we encourage you to use it in your custom Hashers.

### Class Methods

!!! Warning
    Currently scrat can't does not include any binded argument (such as `self`) to the hash. We plan to add this feature shortly.
