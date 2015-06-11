# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import cute_testing
from python_toolbox import sequence_tools

from python_toolbox.sequence_tools import CuteRange

infinity = float('inf')


def test():
    for x, y in zip((CuteRange(10.4, -float('inf'), -7.1)[:5]),
                    (10.4, 3.3, -3.8, -10.9, -18.0, -25.1)):
        assert abs(x - y) < 0.000001


def test_finite():
    finite_range_arguments_tuples = (
        (10,), (3,), (20, 30), (20, 30, 2), (20, 30, -2)
    )
    
    for finite_range_arguments_tuple in finite_range_arguments_tuples:
        cr0 = CuteRange(*finite_range_arguments_tuple)
        assert type(cr0) == CuteRange
        
def test_infinite():
    infinite_range_arguments_tuples = (
        (), (10, infinity), (10, infinity, 2), (100, -infinity, -7)
    )
    
    for infinite_range_arguments_tuple in infinite_range_arguments_tuples:
        cr0 = CuteRange(*infinite_range_arguments_tuple)
        assert type(cr0) == CuteRange
        assert not isinstance(cr0, xrange)
        assert isinstance(cr0, CuteRange)
        assert cr0.length == infinity and len(cr0) == 0
        assert isinstance(cr0[0], int)
        assert cr0[10:].length == cr0[200:].length == infinity
        assert sequence_tools.get_length(cr0[:10]) != infinity != \
                                           sequence_tools.get_length(cr0[:200])
        
def test_illegal():
    illegal_range_arguments_tuples = (
        (infinity, 10, -7), 
    )
    
    for illegal_range_arguments_tuple in illegal_range_arguments_tuples:
        with cute_testing.RaiseAssertor(TypeError):
            CuteRange(*illegal_range_arguments_tuple)
    
        
def test_float():
    cr = CuteRange(10, 20, 1.5)
    assert list(cr) == [10, 11.5, 13, 14.5, 16, 17.5, 19]
    for item in list(cr):
        assert item in cr
    assert 20 not in cr
    assert 20.5 not in cr
    assert 8.5 not in cr
    assert cr.length == len(list(cr)) == 7
    assert list(map(cr.__getitem__, xrange(7))) == list(cr)
    
    float_range_arguments_tuples = (
        (10, 20, 1.5), (20, 10.5, -0.33), (10.3, infinity, 2.5),
        (100, -infinity, -7.1), (10.5, 20)
    )
    
    for float_range_arguments_tuple in float_range_arguments_tuples:
        cr0 = CuteRange(*float_range_arguments_tuple)
        assert type(cr0) == CuteRange
        assert not isinstance(cr0, xrange)
        assert isinstance(cr0, CuteRange)
        assert float in list(map(type, cr0[:2]))
        
        
def test_short_repr():
    assert CuteRange(7, 10).short_repr == '7..9'
    assert CuteRange(7, 10, 3).short_repr == 'CuteRange(7, 10, 3)'
    assert CuteRange(-8, infinity).short_repr == '-8..inf'
    assert CuteRange(8, -infinity, -1).short_repr == 'CuteRange(8, -inf, -1)'
    