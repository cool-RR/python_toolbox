import garlicsim.data_structures


class State(garlicsim.data_structures.State):
    
    def __init__(self):
        pass
        
    @staticmethod
    def create_root():
        return State()
    