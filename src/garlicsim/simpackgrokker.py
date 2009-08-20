class SimpackGrokker(object):
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
    