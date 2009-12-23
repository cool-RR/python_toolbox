# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the Event class.

See its documentation for more information.
'''

import copy
import types

class Event(object):
    '''
    An event.
    
    An event has a `.time_left` property, saying how much time there is until
    the event happens, and an `.action` property which gets called when the
    event happens.
    '''
    def __init__(self, time_left, action):
        assert time_left > 0
        self.time_left = time_left
        self.action = action
        self.done = False
        
    def pass_time(self, t):
        '''
        Make `t` time pass.
        
        If enough time passes, the event happens and the action gets executed.
        In that case the return value of the action will be returned.
        '''
        self.time_left -= t
        if (self.time_left <= 0)  and (not self.done):
            return self.action()
        else:
            return None
        