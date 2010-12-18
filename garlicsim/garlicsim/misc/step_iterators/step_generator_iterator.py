# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `StepGeneratorIterator` class.

See its documentation for more information.
'''


import copy

import garlicsim
from garlicsim.misc import BaseStepIterator, SimpackError, AutoClockGenerator


class StepGeneratorIterator(BaseStepIterator):
    '''
    An iterator that uses a simpack's step generator to produce states.
    
    A step iterator uses the simpack's original step function (or generator)
    under the hood. Using a step iterator instead of using the simpack's step
    has a few advantages:
    
    1. The step iterator automatically adds clock readings if the states are
       missing them.
    2. It's possible to change the step profile while iterating.    
    3. Unless the step function raises `WorldEnded` to end the simulation, this
       iterator is guaranteed to be infinite, even if the simpack's iterator is
       finite.
    
    And possibly more.  
    '''
    
    def __init__(self, state, step_profile):
        
        self.current_state = state
        
        self.step_profile = step_profile
        
        self.step_function = step_profile.step_function
        
        self.__build_raw_iterator()
                    
        self.auto_clock_generator = AutoClockGenerator()
        
        self.auto_clock_generator.make_clock(self.current_state)
            
        self.step_profile_changed = False
        
            
    def __build_raw_iterator(self):
        self.raw_iterator = self.step_profile.step_function(
            self.current_state,
            *self.step_profile.args,
            **self.step_profile.kwargs
        )
    
    
    def next(self):
        '''Crunch the next state.'''
        try:        
            try:
                self.current_state = self.raw_iterator.next()
            except StopIteration:
                self.__build_raw_iterator()
                self.current_state = self.raw_iterator.next()
        except StopIteration:
                raise SimpackError('The step generator %s raised '
                                   '`StopIteration` without yielding even one '
                                   'state.' % self.step_profile.step_function)
                
        self._auto_clock(self.current_state)
        return self.current_state
                
        
    def _auto_clock(self, state):
        '''If the state has no clock reading, give it one automatically.'''
        state.clock = self.auto_clock_generator.make_clock(state)
        

    
