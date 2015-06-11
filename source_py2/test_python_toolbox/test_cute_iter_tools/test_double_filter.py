# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import nifty_collections

from python_toolbox.cute_iter_tools import double_filter


def test_double_filter():
    
    (first_iterable, second_iterable) = \
                        double_filter(lambda value: value % 2 == 0, xrange(20))
    assert tuple(first_iterable) == tuple(xrange(0, 20, 2))
    assert tuple(second_iterable) == tuple(xrange(1, 20, 2))
    
    (first_iterable, second_iterable) = \
                        double_filter(lambda value: value % 3 == 0, range(20))
    assert tuple(first_iterable) == tuple(range(0, 20, 3))
    assert tuple(second_iterable) == tuple(i for i in range(20) if i % 3 != 0)
    
    (first_lazy_tuple, second_lazy_tuple) = \
        double_filter(lambda value: value % 3 == 0, range(20), lazy_tuple=True)
    
    assert isinstance(first_lazy_tuple, nifty_collections.LazyTuple)
    assert isinstance(second_lazy_tuple, nifty_collections.LazyTuple)
    assert first_lazy_tuple.collected_data == \
                                         second_lazy_tuple.collected_data == []
    
    assert first_lazy_tuple == nifty_collections.LazyTuple(range(0, 20, 3))
    assert second_lazy_tuple == nifty_collections.LazyTuple(
        i for i in range(20) if i % 3 != 0
    )
    