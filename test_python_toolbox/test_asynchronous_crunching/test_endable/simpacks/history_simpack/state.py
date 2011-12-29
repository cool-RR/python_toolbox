import garlicsim.data_structures
from garlicsim.misc import WorldEnded

class State(garlicsim.data_structures.State):
    
    def __init__(self):
        pass
    
    @staticmethod
    def history_step(history_browser):
        assert isinstance(history_browser, garlicsim.misc.BaseHistoryBrowser)
        last_state = history_browser.get_last_state()
        last_state_clock = getattr(last_state, 'clock', 0)
        if last_state_clock >= 4:
            raise WorldEnded
        new_state = State()
        new_state.clock = last_state_clock + 1
        return new_state
        
    @staticmethod
    def create_root():
        return State()
    