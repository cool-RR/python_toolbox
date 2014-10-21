# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

import collections
import multiprocessing.queues
import queue as queue_module

from python_toolbox import nifty_collections
from python_toolbox.nifty_collections import Ordered, DefinitelyUnordered


def _make_instance_of_type(type_):
    argument_packs_to_try = (
        (),
        ({'a': 0, 'b': 1, 'c': 2,},),
        ('hello',),
        (b'hello', ),
        (lambda: 7, ((0, 1),))
    )
    for argument_pack_to_try in argument_packs_to_try:
        try:
            return type_(*argument_pack_to_try)
        except (TypeError, ValueError):
            pass
    else:
        raise RuntimeError
    
    

def test():
    ordereds = {
        list, tuple, str, bytearray, bytes,
        nifty_collections.OrderedDict, collections.OrderedDict,
        nifty_collections.OrderedBag, nifty_collections.FrozenOrderedBag, 
        queue_module.Queue, collections.deque
    }
    definitely_unordereds = {
        set, frozenset, collections.defaultdict, collections.Counter,
        nifty_collections.Bag, nifty_collections.FrozenBag
    }
    other_unordereds = {iter({1, 2, 3}), iter({1: 2,}), iter(frozenset('abc'))}
    
    things = ordereds | definitely_unordereds | other_unordereds
    
    for thing in things:
        if isinstance(thing, type):
            type_ = thing
            instance = _make_instance_of_type(type_)
        else:
            instance = thing
            type_ = type(thing)
            
        assert issubclass(type_, Ordered) == (thing in ordereds)
        assert isinstance(instance, Ordered) == (thing in ordereds)
        
        assert issubclass(type_, DefinitelyUnordered) == \
                                               (thing in definitely_unordereds)
        assert isinstance(instance, DefinitelyUnordered) == \
                                               (thing in definitely_unordereds)
        
        