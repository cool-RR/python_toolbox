import garlicsim.data_structures


class State(garlicsim.data_structures.State):
    
    def __init__(self):
        pass
    
    def step(self):
        return State()
    
    def step_generator(self):
        current_state = self
        while True:
            current_state = current_state.step()
            yield current_state
        
    @staticmethod
    def create_root():
        return State()
    