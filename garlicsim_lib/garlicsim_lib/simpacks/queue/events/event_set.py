# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `EventSet` class.

See its documentation for more information.
'''

from .event import Event


class EventSet(object):
    '''A set of events that happen in the same "world".'''
    
    def __init__(self):
        self.events = []
        '''Sorted list of all the events in the system.'''
    
        
    def create_event(self, time_left, action):
        '''
        Create a new event in this event set.

        Returns the new event.
        '''
        event = Event(time_left, action)
        
        self.events.append(event)
        self.events.sort(key=Event._get_time_left)
        
        return event

    
    def do_next_event(self):
        '''
        Pass the time until the closest pending event(s), making them happen.
        
        Return the amount of time that was passed.
        '''
        if not self.events:
            raise Exception('No pending events.')
        
        first_event = self.events.pop()
        simultaneous_events = [first_event]
        time_to_next_event = first_event.time_left
        
        while True:
            if self.events[0].time_left == time_to_next_event:
                simultaneous_events.append(self.events.pop(0)
            
        closest_event = self.get_closest_event()
        
        closest_event_time_left = closest_event.time_left
        self.events.remove(closest_event)
        for event in self.events:
            event.pass_time(closest_event_time_left)
            assert event.time_left > 0 # making sure no other event gets done
        closest_event.pass_time(closest_event_time_left)
        
        return closest_event_time_left
    
    
    def get_closest_event(self):
        '''Get the closest pending event.'''
        return min(self.events, key=lambda event: event.time_left) if \
               self.events else None