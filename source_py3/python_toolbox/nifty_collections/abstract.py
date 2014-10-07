import abc
import collections

class Ordered(metaclass=abc.ABCMeta):
    __slots__ = ()


Ordered.register(collections.Sequence)
Ordered.register(collections.OrderedDict)