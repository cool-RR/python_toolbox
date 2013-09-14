# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `sequence_tools.parse_slice`.'''

from python_toolbox import math_tools

from python_toolbox.sequence_tools import parse_slice


infinity = float('inf')


def test():
    '''Test the basic workings of `parse_slice`.'''
    
    r1 = list(range(5))
    r2 = list(range(2, 10))
    r3 = list(range(100, 3, -7))
    ranges = [r1, r2, r3]
    
    slices = [slice(3), slice(5), slice(9), slice(1, 4), slice(4, 7),
              slice(6, 2), slice(1, 4, 1), slice(1, 5, 3), slice(6, 2, 3),
              slice(6, 2, -3),  slice(8, 2, -1), slice(2, 5, -2),
              slice(None, 5, -2), slice(6, None, -2), slice(8, 4, None),
              slice(None, None, -2)]
    
    for slice_ in slices:
        (start, stop, step) = parse_slice(slice_)
        
        # Replacing `infinity` with huge number cause Python's lists can't
        # handle `infinity`:
        if abs(start) == infinity: start = 10**10 * math_tools.get_sign(start)
        if abs(stop) == infinity: stop = 10**10 * math_tools.get_sign(stop)
        if abs(step) == infinity: step = 10**10 * math_tools.get_sign(step)
        #######################################################################
            
        assert [start, stop, step].count(None) == 0
        
        parsed_slice = slice(start, stop, step)
        for range_ in ranges:
            assert range_[slice_] == range_[parsed_slice]