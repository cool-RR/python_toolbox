# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `HistoryStepIterator` class.

See its documentation for more information.
'''

import garlicsim
from garlicsim.misc import BaseStepIterator, SimpackError, AutoClockGenerator


class HistoryStepIterator(BaseStepIterator):
    '''
    An iterator that uses a simpack's history step function to produce states.
    
    The step iterator automatically adds `.clock` readings if the states
    produced by the step function are missing them.
    '''
    
    def __init__(self, history_browser, step_profile):
        
        assert isinstance(history_browser, garlicsim.misc.BaseHistoryBrowser)
        self.history_browser = history_browser
        '''The history browser that the history step function will use.'''
        
        self.history_step_function = step_profile.step_function
        '''The history step function that will produce states for us.'''
        
        self.step_profile = step_profile
        '''
        The step profile which contains the arguments given to step function.
        '''
           
        self.auto_clock_generator = AutoClockGenerator()
        '''Auto-clock generator which ensures all states have `.clock`.'''
        
        self.auto_clock_generator.make_clock(
            self.history_browser.get_last_state()
        )
        
    
    def next(self):
        '''Crunch the next state.'''
        state = self.history_step_function(
            self.history_browser,
            *self.step_profile.args,
            **self.step_profile.kwargs
        )
        self._auto_clock(state)
        return state
    
        
    def _auto_clock(self, state):
        '''If the state has no clock reading, give it one automatically.'''
        state.clock = self.auto_clock_generator.make_clock(state)

    
