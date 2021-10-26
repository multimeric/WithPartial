# WithPartial
## Introduction

WithPartial is a simple utility for functional piping in Python.
The package exposes a context manager (used with `with`) called `PipeContext`, that allows you to access any function in any scope as a partial, meaning that it's naturally pipeable.
Here's a contrived example from the test suite:

```python
import numpy as np
from with_partial import PartialContext
from pipetools import pipe

with PartialContext() as _:
    ret = (
            10 > pipe |
            _.np.ones() |
            _.np.reshape(newshape=(5, 2)) |
            _.np.mean() |
            _.int()
    )
    assert ret == 1
```

As you can see, we were able to call both `numpy` and built-in functions on the `_` object, and it executed the pipeline similarly to say R's `magrittr` package.

## Installation
```bash
pip install with_partial
```

## Usage
Actually WithPartial doesn't provide an actual piping mechanism, but it does add a useful syntax for use with pipes.
For the actual piping mechanism, I suggest that you try [pipetools](https://0101.github.io/pipetools/doc/index.html), which this package is actually tested against.

WithPartial provides a single class: `PipeContext`.
The way you use `PipeContext` is by first using it as a context manager:
```python
with PipeContext() as _:
```

Then, using the return value of the context manager, which we have named `_` (but you could call it anything), you access attributes and items (using `.attr` or `["key"]` or `[0]`) to locate the function you want and then you finally call it `()`, which will create the partial.
You can use positional and keyword arguments at this point if you need

For more usage information, refer to the [test suite](https://github.com/multimeric/WithPartial/tree/master/test).

## Tests

Note: you will need [poetry](https://python-poetry.org/docs/pyproject/) installed.

```bash
git clone https://github.com/multimeric/WithPartial.git
cd WithPartial
poetry install --extras pipetools
poetry run pytest test/
```