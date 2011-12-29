import garlicsim.data_structures


class State(garlicsim.data_structures.State):
    
    def __init__(self):
        pass
    
    @staticmethod
    def history_step(history_browser):
        return State()
        
    @staticmethod
    def create_root():
        return State()
    