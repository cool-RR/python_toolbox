import abc
import collections
import queue
import multiprocessing.queues


class Ordered(metaclass=abc.ABCMeta):
    __slots__ = ()


Ordered.register(collections.Sequence)
Ordered.register(collections.OrderedDict)
Ordered.register(collections.deque)
Ordered.register(queue.Queue)
Ordered.register(multiprocessing.queues.Queue)