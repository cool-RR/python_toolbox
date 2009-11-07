# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the SimpackGrokker class and the InvalidSimpack exception.
See their documentation for more details.
'''

import functools

from garlicsim.misc import AutoClockGenerator
import garlicsim

__all__ = ["SimpackGrokker", "InvalidSimpack"]

class InvalidSimpack(Exception):
    '''
    An exception to raise when trying to load an invalid simpack.
    '''
    pass

class SimpackGrokker(object):
    '''
    An object that encapsulates a simpack, giving useful information about it
    and tools to use with it.
    '''
    def __init__(self, simpack):
        self.simpack = simpack
        self.__init_analysis()
    
    def __init_analysis(self):
        '''
        Analyze the simpack.
        '''
        simpack = self.simpack
        self.simple_non_history_step_defined = hasattr(simpack, "step")
        self.non_history_step_generator_defined = \
            hasattr(simpack, "step_generator")
        self.simple_history_step_defined = hasattr(simpack, "history_step")
        self.history_step_generator_defined = hasattr(simpack,
                                                      "history_step_generator")
        
        self.non_history_step_defined = \
            (self.simple_non_history_step_defined or \
             self.non_history_step_generator_defined)
        
        self.history_step_defined = (self.simple_history_step_defined or \
                                     self.history_step_generator_defined)
        
        self.simple_step_defined = (self.simple_non_history_step_defined or \
                                    self.simple_history_step_defined)
        
        self.step_generator_defined = \
            (self.non_history_step_generator_defined or \
             self.history_step_generator_defined)
        
        if self.history_step_defined and self.non_history_step_defined:
            raise InvalidSimpack('''The simulation package is defining both a \
            history-dependent step and a non-history-dependent step - which \
            is forbidden.''')
        
        if not (self.simple_step_defined or self.step_generator_defined):
            raise InvalidSimpack('''The simulation package has not defined any
            kind of step function.''')
        
        self.history_dependent = self.history_step_defined
        
        
        
    def step(self, state_or_history_browser, step_profile):
        '''tododoc'''
        auto_clock_generator = AutoClockGenerator()
        if isinstance(state_or_history_browser,
                      garlicsim.data_structures.State):
            state = state_or_history_browser
        else:
            state = state_or_history_browser.get_last_state()
        auto_clock_generator.make_clock(state)

        if self.simple_step_defined:
            step_function = self.simpack.history_step if \
                          self.history_dependent else self.simpack.step
            result = step_function(state_or_history_browser,
                                   *step_profile.args,
                                   **step_profile.kwargs)
        else:# self.step_generator_defined is True
            step_generator = self.simpack.history_step_generator if \
                          self.history_dependent else \
                          self.simpack.step_generator
            iterator = step_generator(state_or_history_browser,
                                      *step_profile.args,
                                      **step_profile.kwargs)
            result = iterator.next()
            
        result.clock = AutoClockGenerator.make_clock(result)
        return result
            
        
    
    def step_generator(self, state_or_history_browser, step_profile):
        '''tododoc'''
        
        if self.step_generator_defined:
            step_generator = self.simpack.history_step_generator if \
                           self.history_dependent else \
                           self.simpack.step_generator
            return KewlIterator(state_or_history_browser, step_profile,
                                step_generator=step_generator)
        else:
            assert self.simple_step_defined
            simple_step = self.simpack.history_step if self.history_dependent \
                        else self.simpack.step
            return KewlIterator(state_or_history_browser, step_profile,
                                simple_step=simple_step)
        

import copy
import garlicsim

class KewlIterator(object):
    '''
    tododoc
    
    make stuff private here?
    '''
    def __init__(self, state_or_history_browser, step_profile,
                 simple_step = None, step_generator=None):

        assert [simple_step, step_generator].count(None) == 1
        
        self.simple_step = simple_step
        self.step_generator = step_generator
        self.raw_iterator = None
        
        self.step_profile = copy.deepcopy(step_profile)
        self.history_dependent = isinstance(state_or_history_browser,
                                            garlicsim.misc.HistoryBrowser)
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
        '''
        '''
        self.current_state = self.__get_new_state()
        self.auto_clock(self.current_state)
        #raise StandardError(str(self.current_state.clock))
        return self.current_state
        
    def __get_new_state(self):
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
                    raise InvalidSimpack('''Step generator's iterator raised
StopIteration before producing a single state.''')
            
                
    def rebuild_raw_iterator_if_necessary(self):
        if (self.raw_iterator is None) or self.step_profile_changed:
            self.rebuild_raw_iterator()
            self.step_profile_changed = False
            
    def rebuild_raw_iterator(self):
        thing = self.current_state or self.history_browser
        self.raw_iterator = self.step_generator(thing,
                                                *self.step_profile.args,
                                                **self.step_profile.kwargs)
                
        
        
    def auto_clock(self, state):
        value = self.auto_clock_generator.make_clock(state)
        state.clock = value
        
    def set_step_profile(self, step_profile):
        self.step_profile = copy.deepcopy(step_profile)
        self.step_profile_changed = True
        
    
    
    
    
