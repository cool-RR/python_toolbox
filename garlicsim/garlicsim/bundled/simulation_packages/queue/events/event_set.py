# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the EventSet class.

See its documentation for more information.
'''

import numpy

from event import Event

class EventSet(object):
    '''A set of events that happen in the same "world".'''
    def __init__(self):
        self.events = []
        pass
    
    def create_event(self, *args, **kwargs):
        '''
        Create a new event in this event set.

        Returns the new event.
        '''
        event = Event(*args, **kwargs)
        self.events.append(event)
        return event
        
    def do_next_event(self):
        '''
        Pass the time until the closest pending event, making it happen.
        
        Return the amount of time that was passed.
        '''
        closest_event = self.get_closest_event()
        if closest_event is None:
            raise Exception('No pending events.')
        closest_event_time_left = closest_event.time_left
        self.events.remove(closest_event)
        for event in self.events:
            event.pass_time(closest_event_time_left)
            assert event.time_left > 0 # making sure no other event gets done
        closest_event.pass_time(closest_event_time_left)
        
        return closest_event_time_left
    
    def get_closest_event(self):
        '''
        Get the closest pending event.
        '''
        if not self.events:
            return None
        times = [event.time_left for event in self.events]
        closest_event = self.events[numpy.argmin(times)]
        return closest_event