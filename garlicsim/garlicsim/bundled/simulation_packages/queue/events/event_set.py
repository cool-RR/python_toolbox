import numpy

from event import Event

class EventSet(object):
    
    def __init__(self):
        self.events = []
        pass
    
    def create_event(self, *args, **kwargs):        
        event = Event(*args, **kwargs)
        self.events.append(event)
        return event
        
    def do_next_event(self):
        
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
        
        if not self.events:
            return None
        times = [event.time_left for event in self.events]
        closest_event = self.events[numpy.argmin(times)]
        return closest_event