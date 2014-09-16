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
        cr0 = CuteRange(*built_in_range_arguments_tuple)
        assert type(cr0) == range
        assert isinstance(cr0, range)
        assert isinstance(cr0, CuteRange)
        cr1 = CuteRange(*built_in_range_arguments_tuple, _avoid_built_in_range=True)
        assert cr1.length == len(cr1)
        assert type(cr1) == CuteRange
        assert not isinstance(cr1, range)
        assert isinstance(cr1, CuteRange)
        assert tuple(cr0) == tuple(cr1)
        if cr0:
            assert cr0[0] == cr1[0]
            assert cr0[-1] == cr1[-1]
        assert repr(cr0)[1:] == repr(cr1)[5:]
        
    infinite_range_arguments_tuples = (
        (), (10, infinity), (10, infinity, 2), (100, -infinity, -7)
    )
    
    for infinite_range_arguments_tuple in infinite_range_arguments_tuples:
        cr0 = CuteRange(*infinite_range_arguments_tuple)
        assert type(cr0) == CuteRange
        assert not isinstance(cr0, range)
        assert isinstance(cr0, CuteRange)
        assert cr0.length == infinity and len(cr0) == 0
        assert isinstance(cr0[0], int)
        
    illegal_range_arguments_tuples = (
        (infinity, 10, -7), 
    )
    
    for illegal_range_arguments_tuple in illegal_range_arguments_tuples:
        with cute_testing.RaiseAssertor(TypeError):
            CuteRange(*illegal_range_arguments_tuple)
    
        
    raise 1 / 0 # Keep testing doge
        
    