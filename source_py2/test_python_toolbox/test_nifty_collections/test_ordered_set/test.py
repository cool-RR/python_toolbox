# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `nifty_collections.ordered_dict.OrderedSet`.'''

from python_toolbox import cute_testing

from python_toolbox.nifty_collections import OrderedSet


def test_sort():
    '''Test the basic workings of `OrderedSet`.'''
    
    ordered_set = OrderedSet(xrange(4))
    
    assert list(ordered_set) == list(range(4))
    assert len(ordered_set) == 4
    assert 1 in ordered_set
    assert 3 in ordered_set
    assert 7 not in ordered_set
    ordered_set.add(8)
    assert list(ordered_set)[-1] == 8
    ordered_set.discard(2)
    assert 2 not in ordered_set
    assert list(reversed(ordered_set)) == [8, 3, 1, 0]
    assert ordered_set.pop() == 8
    assert ordered_set.pop(last=False) == 0
    