# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `Event` class.

See its documentation for more information.
'''


class Event(object):
    '''
    An event which will happen in the future.
    
    An event has a `.time_left` property, saying how much time there is until
    the event happens, and an `.action` property which gets called when the
    event happens.
    '''
    
    def __init__(self, time_left, action):
        assert time_left > 0
        self.time_left = time_left
        self.action = action
        self.done = False

        
    def _get_time_left(self):
        return self.time_left