# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
tododoc
'''

import weakref
import functools

import garlicsim


class StateMemoizedFunction(object):
    '''
    bla bla
    
    bla bla
    bla bla
    '''
    def __init__(self, function):
        self.function = function #todo assert function takes only state arg
        self.memo = weakref.WeakKeyDictionary()

        if self.function.__doc__:
            self.__doc__ += \
            '\nThis is the documentation of the original function, `%s`:\n' % \
            self.function.__name__+ self.function.__doc__
        
        
    def __call__(self, state):
        assert isinstance(state, garlicsim.data_structures.State)
        if state in self.memo:
            return self.memo[state]
        else:
            self.memo[state] = value = self.function(state)
            return value
        
    def purge(self):
        self.memo.clear()
        
'''
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
'''

def history_memoize(function, *args, **kwargs):
    pass

if __name__ == '__main__':
    @StateMemoizedFunction
    def f(state):
        '''
        Calculate the puke of the function.
        
        Puke is very tasty.
        '''
        import random
        return random.random()
    
    s1 = garlicsim.data_structures.State()
    s2 = garlicsim.data_structures.State()
    
    print(f(s1), f(s2), f(s1), f(s2), f(s1), f(s2))
    