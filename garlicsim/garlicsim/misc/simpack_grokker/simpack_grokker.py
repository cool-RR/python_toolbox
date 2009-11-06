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
        self.__init_step()
        self.step.history_dependent = self.history_step_defined
        self.__init_step_generator()
    
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
        
    def __init_step_generator(self):
        '''
        Obtain a step generator.tododoc
        
        If the simpack defines one, use it, otherwise create one from the simple
        step function.
        '''
        if self.step_generator_defined:
            # The simpack supplies a step generator, so we're gonna use that.
            if self.history_step_defined:
                self.step_generator = self.simpack.history_step_generator
                return
            else: # It's a non-history simpack
                self.step_generator = self.simpack.step_generator
                return
                
        else:
            '''
            The simpack supplied no step generator, only a simple step, so
            we're gonna make a generator that uses it.
            Remember, self.step is pointing to our simple step function,
            whether it's history-dependent or not, so we're gonna use self.step
            in our generator.
            '''
            if self.history_step_defined:               
                        
                self.step_generator = functools.partial \
                    (history_step_generator_from_simple_step, self.step)
                return
                
    
            else: # It's a non-history simpack
                
                self.step_generator = functools.partial \
                    (non_history_step_generator_from_simple_step, self.step)
                return
    
    def __init_step(self):
        '''tododoc
        Obtain a simple step function; If the simpack defines one, use it,
        otherwise create one from the step generator.
        '''
        
        
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
        auto_clock_generator = AutoClockGenerator()
        if isinstance(state_or_history_browser,
                      garlicsim.data_structures.State):
            state = state_or_history_browser
        else:
            state = state_or_history_browser.get_last_state()
        auto_clock_generator.make_clock(state)

        if self.step_generator_defined:
            
            step_generator = self.simpack.history_step_generator if \
                          self.history_dependent else \
                          self.simpack.step_generator

            while True: # wrapping it 'cause maybe the iterator is finite
                iterator = step_generator(state_or_history_browser,
                                          *step_profile.args,
                                          **step_profile.kwargs)
                
                for current_state in iterator:
                    current_state.clock = auto_clock_generator(state)
                    yield current_state
                
                if isinstance(state_or_history_browser,
                              garlicsim.data_structures.State):
                    state_or_history_browser = current_state
            
        else: # self.simple_step_defined is True
            
            step_function = self.simpack.history_step if \
                          self.history_dependent else self.simpack.step
            
            if self.history_dependent:
                while True
                
            result = step_function(state,
                                   *step_profile.args,
                                   **step_profile.kwargs)
            current_state = state
            
            result = iterator.next()
            
        result.clock = AutoClockGenerator.make_clock(result)
        return result

import copy
import garlicsim
class KewlIterator(object):
    def __init__(self, step, state_or_history_browser, step_profile):
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
            
    def __iter__(self): return self
    
    def next(self):
        if not self.history_dependent:
            new_state = 
            pass
        else: # self.history_dependent is True
            pass
        
    def auto_clock(self, state):
        state.clock = self.auto_clock_generator.make_clock(state)
        
    def set_step_profile(self, step_profile):
        self.step_profile = copy.deepcopy(step_profile)
        
    
    
    
    
