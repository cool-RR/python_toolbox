# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the AutoClockGenerator class.

See its documentation for more info.
'''

from garlicsim.general_misc.third_party.decorator import decorator

__all__ = ['AutoClockGenerator']

@decorator
def store(method, *args, **kwargs):
    '''Decorator for saving current state's clock for next autoclocking.'''
    self = args[0]
    result = method(*args, **kwargs)
    self.last_state_clock = result
    return result
    
class AutoClockGenerator(object):
    '''Device for creating clock readings for states that don't have them.'''
    def __init__(self):
        self.last_state_clock = None
    
    @store
    def make_clock(self, state):
        '''
        Obtain a clock reading for given state.
        
        If the state already has one, return it; If not, return the clock
        reading of the last state plus one; If this is the first state, return
        0.
        
        Important: The new clock is not added to the state. The state is not
        modified at all. The clock reading is merely returned and the user may
        attach it to the state himself.
        '''
        if hasattr(state, 'clock'):
            return state.clock
        else:
            if self.last_state_clock is not None: # can be 0
                return self.last_state_clock + 1
            else:       
                return 0
            
            