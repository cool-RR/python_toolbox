import garlicsim.data_structures


class State(garlicsim.data_structures.State):
    
    def __init__(self):
        pass
    
    def step(self):
        return State()
    
    def step_generator(self):
        yield State()
        raise StopIteration
        
    @staticmethod
    def create_root():
        return State()
    