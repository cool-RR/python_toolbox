import garlicsim.data_structures


class State(garlicsim.data_structures.State):
    
    def __init__(self):
        pass
    
    def ooga_booga(self):
        return State()
    ooga_booga.step_type = garlicsim.misc.simpack_grokker.step_types.SimpleStep
        
    @staticmethod
    def create_root():
        return State()
    