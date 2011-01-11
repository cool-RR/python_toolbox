# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `DuplicatingStepGeneratorIterator` class.

See its documentation for more information.
'''

import copy

import garlicsim
from garlicsim.misc import BaseStepIterator, SimpackError, AutoClockGenerator


class DuplicatingStepGeneratorIterator(BaseStepIterator):
    '''
    An iterator that uses a simpack's inplace step generator to produce states.
    
    Despite the fact that this iterator uses an *inplace* step generator under
    the hood, it produces a new distinct state on every iteration. It does that
    by deepcopying the state on every iteration.
    
    The step iterator automatically increments the state's `.clock` by 1 if the
    original step generator doesn't change the `.clock` itself.
    '''
    
    def __init__(self, state, step_profile):
        
        self.current_state = state
        '''
        The current state that will be crunched from on the next iteration.
        '''
        
        self._state_of_raw_generator = None
                
        assert garlicsim.misc.simpack_grokker.step_types.InplaceStepGenerator.\
               __instancecheck__(step_profile.step_function)
        
        self.step_function = step_profile.step_function
        '''The step function that will perform step for us.'''
        
        self.step_profile = step_profile
        '''
        The step profile which contains the arguments given to step function.
        '''
        
        self.auto_clock_generator = AutoClockGenerator(detect_static=True)
        '''Auto-clock generator which ensures all states have good `.clock`.'''
        
        self.auto_clock_generator.make_clock(self.current_state)
        
        self.__build_raw_generator()

    
    def __build_raw_generator(self):
        '''Build a raw generator which will perform step for us.'''
        self._state_of_raw_generator = \
            garlicsim.misc.state_deepcopy.state_deepcopy(self.current_state)
        self.raw_generator = self.step_profile.step_function(
            self._state_of_raw_generator,
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
                
            self._auto_clock(self._state_of_raw_generator)
                
            self.current_state = garlicsim.misc.state_deepcopy.state_deepcopy(
                self._state_of_raw_generator
            )
            
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
        

    
