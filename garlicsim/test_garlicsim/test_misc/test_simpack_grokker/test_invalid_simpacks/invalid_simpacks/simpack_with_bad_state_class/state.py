import garlicsim.data_structures


class State(object):
    
    def __init__(self):
        pass
    
    def step(self):
        return State()
        
    @staticmethod
    def create_root():
        return State()
    