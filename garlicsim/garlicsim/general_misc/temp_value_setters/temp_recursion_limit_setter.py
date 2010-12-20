# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `TempRecursionLimitSetter` class.

See its documentation for more details.
'''

import sys

from .temp_value_setter import TempValueSetter


class TempRecursionLimitSetter(TempValueSetter):
    '''
    Context manager for temporarily setting a value to a variable.
    
    The value is set to the variable before the suite starts, and gets reset
    back to the old value after the suite finishes.
    '''
    
    def __init__(self, recursion_limit):
        '''
        Construct the `TempValueSetter`.
        
        `variable` may be either an (`object`, `attribute_string`) pair or a
        `(getter, setter)` pair.
        
        `value` is the temporary value to set to the variable.
        '''
        assert isinstance(recursion_limit, int)
        TempValueSetter.__init__(
            self,
            (sys.getrecursionlimit, sys.setrecursionlimit),
            value=recursion_limit
        )