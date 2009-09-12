"""
A module that defined the SimpackGrokker class. See its documentation
for more details.

todo: separate to two classes according to history-dependence and make
factory function?
"""

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
        
        
        self.non_history_step_defined = (self.simple_step_defined or \
                                         self.step_generator_defined)
        
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
        
        self.step = simpack.step if step_defined else simpack.history_step
        self.history_dependent =  self.step.history_dependent = \
            history_step_defined
        
    
    def step_generator(self, old_state_or_history_browser, *args, **kwargs):
        data = old_state_or_history_browser
        if self.non_history_step_generator_defined:
            return self.simpack.step_generator(data, *args, **kwargs)
        if self.history_step_generator_defined:
            return self.simpack.history_step_generator(data, *args, **kwargs)
        
        return create_step_generator_from_simple_step(self.step, data, *args,
                                                      **kwargs)
    
    

def create_non_history_step_generator_from_simple_step(step_function,
                                                       old_state,
                                                       *args, **kwargs):
    current = old_state
    while True:
        current = step_function(current, *args, **kwargs)
        yield current

def create_history_step_generator_from_simple_step(step_function,
                                                   history_browser,
                                                   *args, **kwargs):
    while True:
        yield step_function(history_browser, *args, **kwargs)

        
