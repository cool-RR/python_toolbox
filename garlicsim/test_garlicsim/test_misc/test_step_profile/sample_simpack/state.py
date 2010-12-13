import garlicsim.data_structures


class State(garlicsim.data_structures.State):
    
    def __init__(self):
        pass
    
    def step(self, a=1, b=2, c=3, *args, **kwargs):
        return State()
    
    def alternate_step(self, x=1, y=2, z=3):
        return State()
    
    @staticmethod
    def create_root():
        return State()
    