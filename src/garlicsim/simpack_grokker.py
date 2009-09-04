"""
A module that defined the SimpackGrokker class. See its documentation
for more details.
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

        step_defined = hasattr(simpack, "step")
        history_step_defined = hasattr(simpack, "history_step")

        if step_defined and history_step_defined:
            raise StandardError("The simulation package is defining both a \
                                 step and a history_step - That's forbidden!")
        
        self.step = simpack.step if step_defined else simpack.history_step
        self.history_dependent =  self.step.history_dependent = \
            history_step_defined
    