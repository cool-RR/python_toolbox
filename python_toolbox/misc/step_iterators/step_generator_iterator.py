# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `StepGeneratorIterator` class.

See its documentation for more information.
'''

import garlicsim
from garlicsim.misc import BaseStepIterator, SimpackError, AutoClockGenerator


class StepGeneratorIterator(BaseStepIterator):
    '''
    An iterator that uses a simpack's step generator to produce states.
    
    A step iterator uses the simpack's original step function (or in this case
    generator) under the hood.
    
    The step iterator automatically adds `.clock` readings if the states
    produced by the step function are missing them.
    
    If the simpack's step generator will terminate, this iterator will make a
    fresh one without alerting the user.
    '''
    
    def __init__(self, state, step_profile):
        
        self.current_state = state
        '''
        The current state that will be crunched from on the next iteration.
        '''
        
        self.step_function = step_profile.step_function
        '''The step generator that will `yield` states for us.'''
        
        
        self.step_profile = step_profile
        '''
        The step profile which contains the arguments given to step function.
        '''
        
        self.auto_clock_generator = AutoClockGenerator()
        '''Auto-clock generator which ensures all states have `.clock`.'''
        
        self.__build_raw_generator()
                    
        self.auto_clock_generator.make_clock(self.current_state)
        
            
    def __build_raw_generator(self):
        '''Build a raw generator which will provide the states for us.'''
        self.raw_generator = self.step_profile.step_function(
            self.current_state,
            *self.step_profile.args,
            **self.step_profile.kwargs
        )
    
    
    def next(self):
        '''Crunch the next state.'''
        try:        
            try:
                self.current_state = self.raw_generator.next()
            except StopIteration:
                self.__build_raw_generator()
                self.current_state = self.raw_generator.next()
        except StopIteration:
                raise SimpackError('The step generator %s raised '
                                   '`StopIteration` without yielding even one '
                                   'state.' % self.step_profile.step_function)
                
        self._auto_clock(self.current_state)
        return self.current_state
                
        
    def _auto_clock(self, state):
        '''If the state has no clock reading, give it one automatically.'''
        state.clock = self.auto_clock_generator.make_clock(state)
        

    
