import operator
import typing
from collections import namedtuple

from with_pipe.partial_proxy import PartialProxy


def dict_to_nt(d: dict, name="tup") -> typing.NamedTuple:
    return namedtuple(name, d.keys())(*d.values())


def test_proxy():
    obj = {"a": {"b": dict_to_nt({"c": None})}}
    p = PartialProxy()["a"]["b"].c
    assert len(p.path) == 3
    assert isinstance(p.path[0], operator.itemgetter)
    assert isinstance(p.path[1], operator.itemgetter)
    assert isinstance(p.path[2], operator.attrgetter)
    assert p.eval(obj) is None
