# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the StepIterator class.

See its documentation for more information.
'''


import copy

import garlicsim
from garlicsim.misc import SimpackError, AutoClockGenerator


class StepIterator(object):
    '''
    An iterator that uses a simpack's step to produce states.
    
    The StepIterator uses under the hood the simpack's step function, be it a
    simple step function or a step generator. Using a StepIterator instead of
    using the simpack's step has a few advantages:
    
    1. The StepIterator automatically adds clock readings if the states are
       missing them.
    2. It's possible to change the step profile while iterating.    
    3. Unless the step function raises `WorldEnd` to end the simulation, this
       iterator is guaranteed to be infinite, even if the simpack's iterator is
       finite.
    
    And possibly more.  
    '''
    # todo: make stuff private here?
    def __init__(self, state_or_history_browser, step_profile,
                 simple_step = None, step_generator=None):
        '''
        Constructor.
        
        The iterator will use either a simple step function or a step generator
        under the hood. You have to supply either one or the other, but not
        both.
        '''

        assert [simple_step, step_generator].count(None) == 1
        
        self.simple_step = simple_step
        self.step_generator = step_generator
        self.raw_iterator = None
        
        self.step_profile = copy.deepcopy(step_profile)
        self.history_dependent = isinstance(state_or_history_browser,
                                            garlicsim.misc.BaseHistoryBrowser)
        if self.history_dependent:
            self.current_state = None
            self.history_browser = state_or_history_browser
        else:
            self.current_state = state_or_history_browser
            self.history_browser = None
            
        self.auto_clock_generator = AutoClockGenerator()
        if self.current_state:
            self.auto_clock_generator.make_clock(self.current_state)
            
        self.step_profile_changed = False
            
    def __iter__(self): return self
    
    def next(self):
        '''Crunch the next state.'''
        self.current_state = self.__get_new_state()
        self.auto_clock(self.current_state)
        return self.current_state
        
    def __get_new_state(self): # todo: rename?
        '''Internal method to crunch the next state.'''
        if self.simple_step:
            thing = self.history_browser if self.history_dependent else \
                  self.current_state
            return self.simple_step(thing,
                                    *self.step_profile.args,
                                    **self.step_profile.kwargs)
        else: # self.step_generator is not None
            self.rebuild_raw_iterator_if_necessary()
            try:
                return self.raw_iterator.next()
            except StopIteration:
                try:
                    self.rebuild_raw_iterator()
                    return self.raw_iterator.next()
                except StopIteration:
                    raise SimpackError('''Step generator's iterator raised
StopIteration before producing a single state.''')
            
                
    def rebuild_raw_iterator_if_necessary(self):
        '''
        Rebuild the internal iterator if necessary.
        
        This is relevant only when we're using a simpack's step generator and
        not its simple step.
        '''
        if (self.raw_iterator is None) or self.step_profile_changed:
            self.rebuild_raw_iterator()
            self.step_profile_changed = False
            
            
    def rebuild_raw_iterator(self):
        '''
        Rebuild the internal iterator.
        
        This is relevant only when we're using a simpack's step generator and
        not its simple step.
        '''
        thing = self.current_state or self.history_browser
        self.raw_iterator = self.step_generator(thing,
                                                *self.step_profile.args,
                                                **self.step_profile.kwargs)
                
        
    def auto_clock(self, state):
        '''If the state has no clock reading, give it one automatically.'''
        state.clock = self.auto_clock_generator.make_clock(state)
        
        
    def set_step_profile(self, step_profile):
        '''
        Set a new step profile for the StepIterator to use.

        The StepIterator will immediately adopt the new step profile, and any
        states that will be crunched from this point on will be crunched using
        the new step profile. (At least until it is changed again.)
        '''
        self.step_profile = copy.deepcopy(step_profile)
        self.step_profile_changed = True
        

    
