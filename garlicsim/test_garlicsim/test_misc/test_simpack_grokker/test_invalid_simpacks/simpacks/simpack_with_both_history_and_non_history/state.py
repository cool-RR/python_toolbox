import garlicsim.data_structures


class State(garlicsim.data_structures.State):
    
    def __init__(self):
        pass
    
    def step(self):
        return State()
    
    @staticmethod
    def history_step(history_browser):
        raise NotImplementedError
        yield None
        
    @staticmethod
    def create_root():
        return State()
    