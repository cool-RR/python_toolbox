# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `StepIterator` class.

See its documentation for more information.
'''

import garlicsim
from garlicsim.misc import BaseStepIterator, SimpackError, AutoClockGenerator


class StepIterator(BaseStepIterator):
    '''
    An iterator that uses a simpack's step function to produce states.
    
    The step iterator automatically adds `.clock` readings if the states
    produced by the step function are missing them.
    '''
    
    def __init__(self, state, step_profile):
        
        self.current_state = state
        '''
        The current state that will be crunched from on the next iteration.
        '''
        
        self.step_function = step_profile.step_function
        '''The step function that will produce states for us.'''
        
        self.step_profile = step_profile
        '''
        The step profile which contains the arguments given to step function.
        '''
        
        self.auto_clock_generator = AutoClockGenerator()
        '''Auto-clock generator which ensures all states have `.clock`.'''
        
        self.auto_clock_generator.make_clock(self.current_state)
        
        
    def next(self):
        '''Crunch the next state.'''
        self.current_state = self.step_function(self.current_state,
                                                *self.step_profile.args,
                                                **self.step_profile.kwargs)
        self._auto_clock(self.current_state)
        return self.current_state
                
        
    def _auto_clock(self, state):
        '''If the state has no clock reading, give it one automatically.'''
        state.clock = self.auto_clock_generator.make_clock(state)
        

    
