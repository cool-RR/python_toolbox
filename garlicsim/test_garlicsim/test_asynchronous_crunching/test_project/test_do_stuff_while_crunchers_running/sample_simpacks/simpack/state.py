import time

import garlicsim.data_structures
from garlicsim.misc import WorldEnd

class State(garlicsim.data_structures.State):
    
    def __init__(self):
        pass
    
    def step(self):
        time.sleep(0.1)
        if getattr(self, 'clock', 0) >= 4:
            raise WorldEnd
        return State()
        
    @staticmethod
    def create_root():
        return State()
    