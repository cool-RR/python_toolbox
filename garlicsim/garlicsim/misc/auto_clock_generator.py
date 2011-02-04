# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `AutoClockGenerator` class.

See its documentation for more info.
'''

from garlicsim.general_misc import decorator_tools


__all__ = ['AutoClockGenerator']


@decorator_tools.decorator
def store(method, *args, **kwargs):
    '''Decorator for saving current state's clock for next autoclocking.'''
    self = args[0]
    result = method(*args, **kwargs)
    self.last_state_clock = result
    return result


class AutoClockGenerator(object):
    '''
    Device for ensuring that states have good clock readings.
    
    This is useful so the user could be lazy and not write code that advances
    the clock reading of a state.
    
    If we get a state with no clock reading, we give it a clock reading of one
    plus the last state's clock reading.
    
    If `detect_static` is set to `True`, we give the same treatment to states
    that have a clock reading which is identical to the last state's.
    '''
    
    def __init__(self, detect_static=False):
        '''
        Construct the auto-clock generator.
        
        If `detect_static` is set to `True`, we also check if a state's clock
        is is identical to the last state's clock. If so we advance it by one.
        '''
        self.last_state_clock = None
        self.detect_static = detect_static
        
        
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
            if not self.detect_static:
                return state.clock
            else: # self.detect_static is True
                if state.clock == self.last_state_clock:
                    return state.clock + 1
                else:
                    return state.clock
        else:
            if self.last_state_clock is not None: # can be 0
                return self.last_state_clock + 1
            else:       
                return 0
            
            