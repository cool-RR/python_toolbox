# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `EventSet` class.

See its documentation for more information.
'''

from garlicsim.general_misc.third_party.sorted_collection import \
                                                          SortedCollection

from .event import Event


class EventSet(object):
    '''A set of events that happen in the same "world".'''
    
    def __init__(self):
        self.events = SortedCollection(key=lambda event: event.time_left)
        '''Sorted sequence of all the events in the system.'''
    
        
    def create_event(self, time_left, action):
        '''
        Create a new event in this event set.

        Returns the new event.
        '''
        event = Event(time_left, action)
        self.events.insert(event)
        return event

    
    def do_next_event(self):
        '''
        Pass the time until the closest pending event(s), making them happen.
        
        Return the amount of time that was passed.
        '''
        if not self.events:
            raise Exception('No pending events.')
        
        simultaneous_events = [self.events]
        time_to_next_event = 
        
        while True:
            if 
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