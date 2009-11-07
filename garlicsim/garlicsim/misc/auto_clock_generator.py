'''tododoc'''

from garlicsim.general_misc.third_party.decorator import decorator

__all__ = ['AutoClockGenerator']

@decorator
def store(method, *args, **kwargs):
    '''
    tododoc
    '''
    self = args[0]
    result = method(*args, **kwargs)
    self.last_state_clock = result
    return result
    
class AutoClockGenerator(object):
    def __init__(self):
        self.last_state_clock = None
    
    @store
    def make_clock(self, state):
        if hasattr(state, 'clock'):
            return state.clock
        else:
            if self.last_state_clock is not None: # can be 0
                return self.last_state_clock + 1
            else:       
                return 0
            
            