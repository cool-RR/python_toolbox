# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''
Defines the `TempRecursionLimitSetter` class.

See its documentation for more details.
'''

import sys

from .temp_value_setter import TempValueSetter


class TempRecursionLimitSetter(TempValueSetter):
    '''
    Context manager for temporarily changing the recurstion limit.

    The temporary recursion limit comes into effect before the suite starts,
    and the original recursion limit returns after the suite finishes.
    '''

    def __init__(self, recursion_limit):
        '''
        Construct the `TempRecursionLimitSetter`.

        `recursion_limit` is the temporary recursion limit to use.
        '''
        assert isinstance(recursion_limit, int)
        TempValueSetter.__init__(
            self,
            (sys.getrecursionlimit, sys.setrecursionlimit),
            value=recursion_limit
        )