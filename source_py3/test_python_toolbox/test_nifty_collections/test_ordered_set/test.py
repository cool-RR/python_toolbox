# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `nifty_collections.ordered_dict.OrderedSet`.'''

from python_toolbox import cute_testing

from python_toolbox.nifty_collections import OrderedSet


def test():
    '''Test the basic workings of `OrderedSet`.'''
    
    ordered_set = OrderedSet(range(4))
    
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
    
    
def test_sort():
    
    ordered_set = OrderedSet([5, 61, 2, 7, 2])
    assert ordered_set == {5, 61, 2, 7}
    ordered_set.move_to_end(61)
    assert list(ordered_set) == [5, 2, 7, 61]
    ordered_set.sort()
    assert list(ordered_set) == [2, 5, 7, 61]
    ordered_set.sort(key=lambda x: -x, reverse=True)
    assert list(ordered_set) == [2, 5, 7, 61]
    
    
