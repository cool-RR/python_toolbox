import time

import garlicsim.data_structures
from garlicsim.misc import WorldEnded


class State(garlicsim.data_structures.State):
    
    def __init__(self):
        pass
    
    def step_generator(self):
        current_state = self
        while True:
            time.sleep(0.1)
            old_clock = getattr(current_state, 'clock', 0)
            current_state = State()
            current_state.clock = old_clock + 1
            yield current_state
    
    def step(self):
        time.sleep(0.1)
        return State()
            
    @staticmethod
    def create_root():
        return State()
    