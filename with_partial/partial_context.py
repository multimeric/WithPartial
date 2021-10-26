import inspect
from dataclasses import dataclass

from with_partial.partial_proxy import PartialProxy
import typing
from functools import partial
import addict


@dataclass()
class _CallPartialProxy(PartialProxy):
    """
    A slightly modified proxy that, when called() will forward its arguments
    and itself to a hook function
    """

    call_hook: typing.Callable = lambda *args, **kwargs: None

    def __call__(self, *args, **kwargs):
        return self.call_hook(self, *args, **kwargs)


class PartialContext:
    """
    A context manager class for accessing functions as partials
    """
    def __init__(self, globs: dict = None, locs: dict = None):
        # Store the locals and globals dictionaries if provided
        if globs is not None or locs is not None:
            self.frame = addict.Dict()
        else:
            self.frame = None
        if globs is not None:
            self.frame.update(globs)
        if locs is not None:
            self.frame.update(locs)

    def __enter__(self):
        # We first get the frame local variables. If they were provided at
        # instantiation time, use those. Otherwise get them using inspect
        if self.frame is None:
            stack = inspect.stack(context=0)
            locs = addict.Dict(__builtins__, stack[1].frame.f_locals)
            del stack
        else:
            locs = self.frame

        # We define our hook function that is called when the user calls()
        # the context manager
        def eval(proxy: PartialProxy, *args, **kwargs) -> typing.Callable:
            # Find the actual function they are trying to call
            func = proxy.eval(locs)
            # Return a partially applied version
            return partial(func, *args, **kwargs)

        # Finally, we return a proxy for the user to access
        return _CallPartialProxy(path=[], call_hook=eval)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass