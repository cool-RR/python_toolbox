import collections
import multiprocessing.queues
import queue

from python_toolbox import nifty_collections
from python_toolbox.nifty_collections import Ordered

def test():
    ordered_types = {list, tuple, str, bytearray, bytes,
                     nifty_collections.OrderedDict, collections.OrderedDict,
                     queue.Queue, multiprocessing.queues.Queue,
                     collections.deque}
    unordered_types = {set, frozenset, collections.ChainMap,
                       collections.defaultdict, collections.Counter}
    
    types = ordered_types | unordered_types
    
    for type_ in types:
        is_ordered = type_ in ordered_types
        assert issubclass(type_, Ordered) == is_ordered
        argument_packs_to_try = (
            (),
            ({'a': 0, 'b': 1, 'c': 2,},),
            ('hello',),
            (b'hello', ),
            (lambda: 7, ((0, 1),))
        )
        for argument_pack_to_try in argument_packs_to_try:
            try:
                instance = type_(*argument_pack_to_try)
            except (TypeError, ValueError):
                pass
            else:
                break
        else:
            raise RuntimeError
                
        assert isinstance(instance, Ordered) == is_ordered
        
    