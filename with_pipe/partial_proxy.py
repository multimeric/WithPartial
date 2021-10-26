import operator
import typing
from dataclasses import dataclass, field


@dataclass
class PartialProxy:
    path: list[typing.Callable] = field(default_factory=list)

    def _then(self, call: typing.Callable) -> "PartialProxy":
        """
        Return a copy of the current proxy, but with a new operation at the end
        :param call: A callable representing this last action
        """
        kwargs = {**self.__dict__, "path": self.path + [call]}
        return self.__class__(**kwargs)

    def eval(self, frame: dict) -> typing.Callable:
        """
        Evaluate the proxy calls on a given object and return the end of the chain
        :param frame: This is a dictionary of frame variables to evaluate on
        """
        current = frame

        # Whenever this is called, access each of the path elements one at a
        # time
        for segment in self.path:
            current = segment(current)

        return current

    def __getattr__(self, item):
        """
        Proxy an attribute get call
        """
        return self._then(operator.attrgetter(item))

    def __getitem__(self, item):
        """
        Proxy an item get call
        """
        return self._then(operator.itemgetter(item))
