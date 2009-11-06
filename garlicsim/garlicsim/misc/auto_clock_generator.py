'''tododoc'''

class AutoClockGenerator(object):
    def __init__(self):
        self.last_state = None
        pass
    def make_clock(self, state):
        try:
            if hasattr(state, 'clock'):
                return state.clock
            else:
                if self.last_state:
                    return self.last_state.clock + 1
                else:       
                    return 0
        finally:
            self.last_state = state