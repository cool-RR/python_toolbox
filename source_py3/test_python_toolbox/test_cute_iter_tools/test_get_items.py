# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `cute_iter_tools.get_items`.'''

import itertools


from python_toolbox.cute_iter_tools import get_items



def test():
    '''Test the basic workings of `get_items`.'''
    
    iterable = iter(range(10))
    assert get_items(iterable, 3) == (0, 1, 2)
    assert get_items(iterable, 0) == ()
    assert get_items(iterable, 2) == (3, 4)
    assert get_items(iterable, 4) == (5, 6, 7, 8)
    assert get_items(iterable, 3) == (9,)
    assert get_items(iterable, 3) == ()
    assert get_items(iterable, 4) == ()