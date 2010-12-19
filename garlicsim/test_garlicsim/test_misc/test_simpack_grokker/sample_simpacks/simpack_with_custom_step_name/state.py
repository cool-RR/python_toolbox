import garlicsim.data_structures


class State(garlicsim.data_structures.State):
    
    def __init__(self):
        pass
    
    @garlicsim.misc.simpack_grokker.step_types.SimpleStep
    def ooga_booga(self):
        return State()
        
    @staticmethod
    def create_root():
        return State()
    