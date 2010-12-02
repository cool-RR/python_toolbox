import garlicsim.data_structures
from garlicsim.misc import WorldEnd

class State(garlicsim.data_structures.State):
    
    def __init__(self):
        pass
    
    def step(self):
        if getattr(self, 'clock', 0) >= 3:
            raise WorldEnd
        return State()
        
    @staticmethod
    def create_root():
        return State()
    