import abc
import collections

class Ordered(metaclass=abc.ABCMeta):
    __slots__ = ()


collections.Sequence.register