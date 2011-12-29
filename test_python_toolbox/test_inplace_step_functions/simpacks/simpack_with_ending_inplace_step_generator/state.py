import garlicsim.data_structures


class State(garlicsim.data_structures.State):
    
    def __init__(self):
        self.list = []
        self.cross_process_persistent = \
            garlicsim.general_misc.persistent.CrossProcessPersistent()
        self.clock = 0

        
    def inplace_step_generator(self):
        self.clock +=1
        yield
            
        
    @staticmethod
    def create_root():
        return State()
    