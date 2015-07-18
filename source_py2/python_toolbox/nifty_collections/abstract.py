# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

import abc
import collections
import Queue as queue
import multiprocessing.queues
import python_toolbox.third_party.collections


###############################################################################

class Ordered():
    '''
    A data structure that has a defined order.
    
    This is an abstract type. You can use `isinstance(whatever, Ordered)` to
    check whether a data structure is ordered. (Note that there will be false
    negatives.)
    '''
    __metaclass__ = abc.ABCMeta
    __slots__ = ()


Ordered.register(bytearray)
Ordered.register(collections.Sequence)
try:
    Ordered.register(collections.OrderedDict)
except AttributeError:
    # Python 2.6
    pass
Ordered.register(python_toolbox.third_party.collections.OrderedDict)
Ordered.register(collections.deque)
Ordered.register(queue.Queue)
Ordered.register(multiprocessing.queues.Queue)

###############################################################################

class DefinitelyUnordered():
    '''
    A data structure that does not have a defined order.
    
    This is an abstract type. You can use `isinstance(whatever,
    DefinitelyUnordered)` to check whether a data structure is unordered. (Note
    that there will be false negatives.)
    '''
    __metaclass__ = abc.ABCMeta
    __slots__ = ()
    
    @classmethod
    def __subclasshook__(cls, type_):
        try:
            OrderedDict = collections.OrderedDict
        except AttributeError:
            # Python 2.6
            OrderedDict = python_toolbox.third_party.collections.OrderedDict
        if cls is DefinitelyUnordered and issubclass(type_, OrderedDict):
            return False
        else:
            return NotImplemented
        

DefinitelyUnordered.register(set)
DefinitelyUnordered.register(frozenset)
DefinitelyUnordered.register(dict)
DefinitelyUnordered.register(collections.defaultdict)
try:
    DefinitelyUnordered.register(collections.Counter)
except AttributeError:
    # Python 2.6
    pass
    