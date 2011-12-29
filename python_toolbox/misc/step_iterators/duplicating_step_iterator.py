# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `DuplicatingStepIterator` class.

See its documentation for more information.
'''

import copy

import garlicsim
from garlicsim.misc import BaseStepIterator, SimpackError, AutoClockGenerator


class DuplicatingStepIterator(BaseStepIterator):
    '''
    An iterator that uses a simpack's inplace step function to produce states.
    
    Despite the fact that this iterator uses an *inplace* step function under
    the hood, it produces a new distinct state on every iteration. It does that
    by deepcopying the state on every iteration.
    
    The step iterator automatically increments the state's `.clock` by 1 if the
    original step function doesn't change the `.clock` itself.
    '''
    
    def __init__(self, state, step_profile):
        
        self.current_state = state
        '''
        The current state that will be crunched from on the next iteration.
        '''
                
        assert garlicsim.misc.simpack_grokker.step_types.InplaceStep.\
               __instancecheck__(step_profile.step_function)
        
        self.step_function = step_profile.step_function
        '''The step function that will perform step for us.'''
        
        self.step_profile = step_profile
        '''
        The step profile which contains the arguments given to step function.
        '''
        
        self.auto_clock_generator = AutoClockGenerator(detect_static=True)
        '''Auto-clock generator which ensures all states have `.clock`.'''
        
        self.auto_clock_generator.make_clock(self.current_state)
        
        
    def next(self):
        '''Crunch the next state.'''
        new_state = \
            garlicsim.misc.state_deepcopy.state_deepcopy(self.current_state)
        
        return_value = self.step_function(new_state,
                                          *self.step_profile.args,
                                          **self.step_profile.kwargs)
        assert return_value is None
        
        self._auto_clock(new_state)
        self.current_state = new_state
        return self.current_state
                
        
    def _auto_clock(self, state):
        '''
        If the step function didn't advance the state's clock, advance it by 1.
        '''
        state.clock = self.auto_clock_generator.make_clock(state)
        

    
