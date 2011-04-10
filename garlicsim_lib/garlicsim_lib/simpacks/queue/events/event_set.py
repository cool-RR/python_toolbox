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
            
        closest_event = self.events.pop(0)
        
        for event in self.events:
            event.time_left -= closest_event.time_left
            
        closest_event.action()
        
        return closest_event.time_left
    