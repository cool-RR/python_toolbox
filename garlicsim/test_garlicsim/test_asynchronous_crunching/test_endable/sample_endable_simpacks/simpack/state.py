import garlicsim.data_structures
from garlicsim.misc import WorldEnded

class State(garlicsim.data_structures.State):
    
    def __init__(self):
        pass
    
    def step(self):
        if getattr(self, 'clock', 0) >= 4:
            raise WorldEnded
        return State()
        
    @staticmethod
    def create_root():
        return State()
    