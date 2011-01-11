# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `InplaceStepGeneratorIterator` class.

See its documentation for more information.
'''

import copy

import garlicsim
from garlicsim.misc import BaseStepIterator, SimpackError, AutoClockGenerator


class InplaceStepGeneratorIterator(BaseStepIterator):
    '''
    Step iterator that uses an inplace step generator to perform step in place.
    
    A step iterator uses the simpack's original step function (or in this case
    inplace step generator) under the hood.
    
    This is an *inplace* step iterator; It doesn't produce new states, it
    modifies an existing one in place. It keeps yielding the same state, except
    it modifies it on each iteration.
    
    The step iterator automatically increments the state's `.clock` by 1 if the
    step generator doesn't change the `.clock` itself.
    
    If the simpack's step generator will terminate, this iterator will make a
    fresh one without alerting the user.
    '''
    
    def __init__(self, state, step_profile):
        
        self.current_state = state
        '''
        The current state that will be crunched from on the next iteration.
        '''
        
        assert garlicsim.misc.simpack_grokker.step_types.InplaceStepGenerator.\
               __instancecheck__(step_profile.step_function)
        
        self.step_function = step_profile.step_function
        '''The step function that will produce states for us.'''
        
        self.step_profile = step_profile
        '''
        The step profile which contains the arguments given to step function.
        '''
        
        self.auto_clock_generator = AutoClockGenerator(detect_static=True)
        '''Auto-clock generator which ensures all states have good `.clock`.'''
        
        self.auto_clock_generator.make_clock(self.current_state)
        
        self.__build_raw_generator()

    
    def __build_raw_generator(self):
        '''Build a raw generator which will perform steps for us.'''
        self.raw_generator = self.step_profile.step_function(
            self.current_state,
            *self.step_profile.args,
            **self.step_profile.kwargs
        )
        
    
    def next(self):
        '''Crunch the next state.'''
        try:        
            try:
                yielded_value = self.raw_generator.next()
            except StopIteration:
                self.__build_raw_generator()
                yielded_value = self.raw_generator.next()
                
            assert yielded_value is None
                
            self._auto_clock(self.current_state)
            
        except StopIteration:
                raise SimpackError('The inplace step generator `%s` raised '
                                   '`StopIteration` without yielding even '
                                   'once.' % self.step_profile.step_function)
                
        return self.current_state
                
        
    def _auto_clock(self, state):
        '''
        If the raw generator didn't advance the state's clock, advance it by 1.
        '''
        state.clock = self.auto_clock_generator.make_clock(state)
        
