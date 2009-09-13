"""
A module that defined the SimpackGrokker class. See its documentation
for more details.
"""

import functools

__all__ = ["SimpackGrokker"]

class SimpackGrokker(object):
    """
    An object that encapsulates a simpack, giving useful information about it
    that may not be directly specified in the simpack.
    
    When a SimpackGrokker loads a simpack, it checks whether it is
    history-dependent. It puts the answer in its attribute `history_dependent`.
    """
    def __init__(self, simpack):
        self.simpack = simpack
        
    
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
            raise StandardError("The simulation package is defining both a \
                                 history-dependent step and a \
                                 non-history-dependent step - That's \
                                 forbidden!")
        
        assert self.simple_step_defined or self.step_generator_defined
        
        
        self.history_dependent = self.history_step_defined
        
        self.__init_step()
        self.step.history_dependent = self.history_step_defined
        
        self.__init_step_generator()
        
    
    def __init_step_generator(self):
        
        if self.step_generator_defined:
            """
            The simpack supplies a step generator, so we're gonna use that.
            """
            if self.history_step_defined:
                self.step_generator = self.simpack.history_step_generator
                return
            else: # It's a non-history simpack
                self.step_generator = self.simpack.step_generator
                return
                
        else:
            """
            The simpack supplied no step generator, only a simple step, so
            we're gonna make a generator that uses it.
            Remember, self.step is pointing to our simple step function,
            whether it's history-dependent or not, so we're gonna use self.step
            in our generator.
            """
            if self.history_step_defined:               
                        
                self.step_generator = functools.partial \
                    (history_step_generator_from_simple_step, self.step)
                return
                
    
            else: # It's a non-history simpack
                
                self.step_generator = functools.partial \
                    (non_history_step_generator_from_simple_step, self.step)
                return
                
        
    def step_generator(self, old_state_or_history_browser, *args, **kwargs):
        raise NotImplementedError
    
    def __init_step(self):
        if self.simple_step_defined:
            """
            If the simpack defines a simple step, we'll just point to that.
            """
            if self.history_dependent:
                self.step = self.simpack.history_step
                return
            else: # It's non-history dependent
                self.step = self.simpack.step
                return
                
        else:
            if self.history_dependent:
                
                self.step = functools.partial \
                    (simple_history_step_from_step_generator,
                     self.simpack.history_step_generator)
                return
                    
            else: # It's non-history dependent
                
                self.step = functools.partial \
                    (simple_non_history_step_from_step_generator,
                     self.simpack.step_generator)
                return
        
        
    def step(self, old_state_or_history_browser, *args, **kwargs):
        raise NotImplementedError
        
    

def non_history_step_generator_from_simple_step(step_function, old_state,
                                                *args, **kwargs):
    current = old_state
    while True:
        current = step_function(current, *args, **kwargs)
        yield current
        
def history_step_generator_from_simple_step(step_function, history_browser,
                                            *args, **kwargs):
    while True:
        yield step_function(history_browser, *args, **kwargs)
        
def simple_non_history_step_from_step_generator(generator, history_browser,
                                                *args, **kwargs):
    iterator = generator(history_browser, *args, **kwargs)
    return iterator.next()

def simple_history_step_from_step_generator(generator, old_state,
                                            *args, **kwargs):
    iterator = generator(old_state, *args, **kwargs)
    return iterator.next()