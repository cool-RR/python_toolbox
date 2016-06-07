# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import abc
import collections
import queue
import multiprocessing.queues


###############################################################################

class Ordered(metaclass=abc.ABCMeta):
    '''
    A data structure that has a defined order.
    
    This is an abstract type. You can use `isinstance(whatever, Ordered)` to
    check whether a data structure is ordered. (Note that there will be false
    negatives.)
    '''
    __slots__ = ()


Ordered.register(collections.Sequence)
Ordered.register(collections.OrderedDict)
Ordered.register(collections.deque)
Ordered.register(queue.Queue)
Ordered.register(multiprocessing.queues.Queue)

###############################################################################

class DefinitelyUnordered(metaclass=abc.ABCMeta):
    '''
    A data structure that does not have a defined order.
    
    This is an abstract type. You can use `isinstance(whatever,
    DefinitelyUnordered)` to check whether a data structure is unordered. (Note
    that there will be false negatives.)
    '''    
    __slots__ = ()
    
    @classmethod
    def __subclasshook__(cls, type_):
        if cls is DefinitelyUnordered and \
                                    issubclass(type_, collections.OrderedDict):
            return False
        else:
            return NotImplemented
        

DefinitelyUnordered.register(set)
DefinitelyUnordered.register(frozenset)
DefinitelyUnordered.register(dict)
DefinitelyUnordered.register(collections.defaultdict)
DefinitelyUnordered.register(collections.Counter)