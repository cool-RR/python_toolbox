# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
tododoc
'''

import weakref
import functools

import garlicsim

#from garlicsim.general_misc.third_party import decorator as decorator_module
from abcs import MemoizedStateFunction, MemoizedHistoryFunction


def state_memoize(function):
    
    def memoized(state):
        assert isinstance(state, garlicsim.data_structures.State)
        if state in memoized.memo:
            return memoized.memo[state]
        else:
            memoized.memo[state] = value = function(state)
            return value
            
    memoized.memo = weakref.WeakKeyDictionary()
    
    functools.update_wrapper(memoized, function)
    
    MemoizedStateFunction.register(memoized) TODO this isn't working
    
    return memoized

def history_memoize(function, *args, **kwargs):
    pass