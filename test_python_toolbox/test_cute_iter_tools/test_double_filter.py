# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox.cute_iter_tools import double_filter


def test_double_filter():
    
    (first_iterable, second_iterable) = \
                        double_filter(lambda value: value % 2 == 0, xrange(20))
    assert tuple(first_iterable) == tuple(xrange(0, 20, 2))
    assert tuple(second_iterable) == tuple(xrange(1, 20, 2))
    
    (first_iterable, second_iterable) = \
                        double_filter(lambda value: value % 3 == 0, xrange(20))
    assert tuple(first_iterable) == tuple(xrange(0, 20, 3))
    assert tuple(second_iterable) == tuple(i for i in xrange(20) if i % 3 != 0)
    