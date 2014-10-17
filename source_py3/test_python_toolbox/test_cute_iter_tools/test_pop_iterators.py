# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

import collections
from python_toolbox import nifty_collections

from python_toolbox.cute_iter_tools import (iterate_pop, iterate_popitem,
                                            iterate_popleft)


def test():
    
    deque = collections.deque(range(10))
    assert tuple(iterate_pop(deque)) == tuple(range(9, -1, -1))
    assert not deque
    
    deque = collections.deque(range(10))
    assert tuple(iterate_popleft(deque)) == tuple(range(10))
    assert not deque
    
    dict_ = {1: 2, 3: 4, 5: 6,}
    assert dict(iterate_popitem(dict_)) == {1: 2, 3: 4, 5: 6,}
    assert not dict_
    
    lazy_tuple = iterate_pop(list(range(5)), lazy_tuple=True)
    assert isinstance(lazy_tuple, nifty_collections.LazyTuple)
    