# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `python_toolbox.cute_iter_tools.shorten`.'''

from __future__ import generator_stop

import pytest

from python_toolbox import nifty_collections
from python_toolbox import cute_iter_tools
from python_toolbox.cute_iter_tools import shorten


infinity = float('inf')


def test():
    '''Test basic workings of `shorten`.'''
    my_range = [0, 1, 2, 3, 4]

    short_iterator = shorten(my_range, 3)
    assert short_iterator.__iter__() is short_iterator

    assert list(shorten(my_range, 0)) == []
    assert list(shorten(my_range, 1)) == list(range(1))
    assert list(shorten(my_range, 2)) == list(range(2))
    assert list(shorten(my_range, 3)) == list(range(3))
    assert list(shorten(my_range, 4)) == list(range(4))

    assert list(shorten(my_range, infinity)) == my_range
    assert list(shorten(iter(my_range), infinity)) == my_range


def test_lazy_tuple():
    my_range = [0, 1, 2, 3, 4]

    lazy_tuple = shorten(my_range, 3, lazy_tuple=True)
    assert isinstance(lazy_tuple, nifty_collections.LazyTuple)
    assert not lazy_tuple.collected_data

    assert tuple(lazy_tuple) == (0, 1, 2)


def test_dont_pull_extra_item():
    '''Test that `shorten` doesn't pull an extra member from the iterable.'''
    def generator():
        yield from [1, 2, 3]
        raise Exception

    pytest.raises(Exception, lambda: list(generator()))

    iterator_1 = shorten(generator(), 4)
    pytest.raises(Exception, lambda: list(iterator_1))

    iterator_2 = shorten(generator(), infinity)
    pytest.raises(Exception, lambda: list(iterator_2))

    iterator_3 = shorten(generator(), 3)
    list(iterator_3) # Pulling exactly three so we avoid the exception.