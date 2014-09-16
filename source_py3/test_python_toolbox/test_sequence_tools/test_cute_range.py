# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import cute_testing

from python_toolbox.sequence_tools import CuteRange

infinity = float('inf')


def test():
    built_in_range_arguments_tuples = (
        (10,), (3,), (20, 30), (20, 30, 2), (20, 30, -2)
    )
    
    for built_in_range_arguments_tuple in built_in_range_arguments_tuples:
        r0 = CuteRange(*built_in_range_arguments_tuple)
        assert type(r0) == range
        assert isinstance(r0, range)
        assert isinstance(r0, CuteRange)
        r1 = CuteRange(*built_in_range_arguments_tuple, _avoid_built_in_range=True)
        assert r1.length == len(r1)
        assert type(r1) == CuteRange
        assert not isinstance(r1, range)
        assert isinstance(r1, CuteRange)
        assert tuple(r0) == tuple(r1)
        if r0:
            assert r0[0] == r1[0]
            assert r0[-1] == r1[-1]
        assert repr(r0)[1:] == repr(r1)[1:]
        
    infinite_range_arguments_tuples = (
        (), (10, infinity), (10, infinity, 2), (100, -infinity, -7)
    )
    
    for infinite_range_arguments_tuple in infinite_range_arguments_tuples:
        r0 = CuteRange(*infinite_range_arguments_tuple)
        assert type(r0) == CuteRange
        assert not isinstance(r0, range)
        assert isinstance(r0, CuteRange)
        assert r0.length == infinity and len(r0) == 0
        assert isinstance(r0[0], int)
        
    illegal_range_arguments_tuples = (
        (infinity, 10, -7), 
    )
    
    for illegal_range_arguments_tuple in illegal_range_arguments_tuples:
        with cute_testing.RaiseAssertor(TypeError):
            CuteRange(*illegal_range_arguments_tuple)
    
        
    raise 1 / 0 # Keep testing doge
        
    