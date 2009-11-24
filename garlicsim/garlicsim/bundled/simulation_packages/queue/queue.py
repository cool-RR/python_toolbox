# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
tododoc
'''

import random
import copy

import numpy
import numpy.random

from garlicsim.general_misc.infinity import Infinity
import garlicsim

def time_for_next_occurence(mean_time_for_next_occurence):
    mean = mean_time_for_next_occurence
    return numpy.random.exponential(scale=mean)

class State(garlicsim.data_structures.State):
    pass

class Event(object):
    def __init__(self, time_left, action):
        assert time_left > 0
        self.time_left = time_left
        self.action = action
        self.done = False
        
    def pass_time(self, t):
        self.time_left -= t
        if (self.time_left <= 0)  and (not self.done):
            return self.action
        else:
            return None
            

class EventSet(object):
    
    def __init__(self):
        self.events = []
        pass
    
    def add_event(self, *args, **kwargs):        
        event = Event(*args, **kwargs)
        self.events.append(event)
        
    def do_next_event(self):
        times = [event.time_left for event in self.events]
        closest_event = self.events[numpy.argmin(times)]
        closest_event_time_left = closest_event.time_left
        closest_event.pass_time(closest_event_time_left)
        self.events.remove(closest_event)
        for event in self.events:
            event.pass_time(closest_event_time_left)
        return closest_event_time_left
        
        

class Server(object):
    def __init__(self, event_set, mean_service):
        self.event_set = event_set
        self.mean_service = mean_service

class Client(object):
    pass

class Population(object):
    def __init__(self, event_set, size=Infinity, mean_arrival=1):
        assert size == Infinity
        self.size = size
        self.mean_arrival = mean_arrival
        self.event_set = event_set
        self.next_arrival = None
        self.schedule_next_arrival()
        
    def schedule_next_arrival(self):
        assert self.next_arrival is None
        time_left = time_for_next_occurence(self.mean_arrival)
        self.event_set.add_event(time_left, self.make_arrival)
    
    def make_arrival(self):
        client = Client()
        1/0
        self.schedule_next_arrival()
    

def make_plain_state(n_servers=3, population_size=Infinity, mean_arrival=1,
                     mean_service=1):
    my_state = State()
    my_state.event_set = EventSet()
    my_state.servers = [Server(event_set=event_set, mean_service=mean_service)
                        for i in range(servers)]
    my_state.population = Population(event_set=event_set, size=population_size,
                                     mean_arrival=mean_arrival)
    return my_state
    
def step(old_state, t=None):
    '''
    todo good idea: t=None means step to next client. If given int just do many
    steps. (What with cut last?)
    '''
    
    assert t is None # for now
    t = time_for_next_occurence(old_state.population.mean_arrival)
    
    new_state = copy.dep(old_state)
    
    return new_state



def make_random_state(width=45, height=25):
    my_state = State()
    my_state.board = Board(width, height, fill="random")
    return my_state

