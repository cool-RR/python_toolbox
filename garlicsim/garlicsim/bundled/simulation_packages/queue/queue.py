# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
tododoc
'''


import Queue
import random
import copy

import numpy
import numpy.random

from garlicsim.general_misc.infinity import Infinity
import garlicsim

import events as events_module



def time_for_next_occurence(mean_time_for_next_occurence):
    mean = mean_time_for_next_occurence
    return numpy.random.exponential(scale=mean)

class State(garlicsim.data_structures.State):
    pass

            
class Server(object):
    def __init__(self, event_set, facility, mean_service):
        
        self.event_set = event_set
        self.facility = facility
        self.mean_service = mean_service
        
        self.current_client = None
        self.finish_service_event = None
    
    def service_client(self, client):
        assert self.current_client is None and \
               self.finish_service_event is None
        self.current_client = client
        time_to_next = time_for_next_occurence(self.mean_service)
        self.finish_service_event = \
            self.event_set.create_event(time_to_next, self.finish_client)
        
    def finish_client(self):
        assert self.current_client is not None
        client = self.current_client 
        self.current_client = None
        self.finish_service_event = None
        self.facility.clients.remove(client)
        self.facility.request_client(self)
        
        
    def is_busy(self):
        return (self.current_client is not None)
    
    def __repr__(self):
        if self.is_busy():
            return 'Server, busy'
        else:
            return 'Server, free' 
        

class Client(object):
    pass

class Facility(object):
    def __init__(self, event_set, servers=[], clients=[]):
        self.event_set = event_set
        self.servers = servers
        self.clients = clients
        self.waiting_clients = clients[:]
        
    def create_server(self, *args, **kwargs):
        new_server = Server(self.event_set, self, *args, **kwargs)
        self.servers.append(new_server)
        return new_server
    
    def add_client(self, client):
        self.clients.append(client)
        self.waiting_clients.append(client)
        if len(self.waiting_clients) == 1:
            idle_servers_iterator = self.idle_servers_generator()
            try:
                idle_server = idle_servers_iterator.next()
                self.waiting_clients.remove(client)
                idle_server.service_client(client)
            except StopIteration:
                pass
            
    def idle_servers_generator(self):
        inner_generator = (server for server in self.servers
                           if (server.is_busy() is False))
        for idle_server in inner_generator:
            yield idle_server
            
    def request_client(self, server):
        assert server.is_busy() is False
        try:
            client = self.waiting_clients.pop(0)
        except IndexError:
            return None
        server.service_client(client)
        
    def __repr__(self):
        return 'facility with %s clients, %s of which stand in queue' % \
               (len(self.clients), len(self.waiting_clients))
        
                    

        

class Population(object):
    def __init__(self, event_set, facility, size=Infinity, mean_arrival=1):
        assert size == Infinity
        self.size = size
        self.mean_arrival = mean_arrival
        self.event_set = event_set
        self.facility = facility
        self.next_arrival = None
        self.schedule_next_arrival()
        
    def schedule_next_arrival(self):
        assert self.next_arrival is None
        time_left = time_for_next_occurence(self.mean_arrival)
        self.next_arrival = self.event_set.create_event(time_left,
                                                        self.make_arrival)
    
    def make_arrival(self):
        client = Client()
        self.facility.add_client(client)
        self.next_arrival = None
        self.schedule_next_arrival()
        return client
    

def make_plain_state(n_servers=3, population_size=Infinity, mean_arrival=1,
                     mean_service=3):
    my_state = State()
    event_set = events_module.EventSet()
    my_state.event_set = event_set
    my_state.facility = Facility(event_set=event_set)
    for i in range(n_servers):
        my_state.facility.create_server(mean_service=mean_service)
    my_state.servers = my_state.facility.servers
    my_state.population = \
            Population(event_set=event_set, facility=my_state.facility,
                       size=population_size, mean_arrival=mean_arrival)

    
    return my_state
    
def step(old_state, t=None):
    '''
    todo good idea: t=None means step to next client. If given int just do many
    steps. (What with cut last?)
    '''
    
    assert t is None # for now
    
    new_state = copy.deepcopy(old_state)
    time_passed = new_state.event_set.do_next_event()
    
    new_state.clock = old_state.clock + time_passed
    
    return new_state



make_random_state = make_plain_state # for now

