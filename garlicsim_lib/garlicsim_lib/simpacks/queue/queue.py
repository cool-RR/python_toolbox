# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Core module for `queue` simpack for simulations in Queueing Theory.
'''

import Queue
import random
import copy

import numpy
import numpy.random

from garlicsim.general_misc.infinity import Infinity
from garlicsim.misc import StepCopy
import garlicsim

import events as events_module


#todo: math error here:
def time_for_next_occurence(mean_time_for_next_occurence):
    '''
    Given a mean time between occurences, generate the time for next occurence.
    
    Only for occurences that obey a Poisson distribution.
    '''
    mean = mean_time_for_next_occurence
    return numpy.random.exponential(scale=mean)


class State(garlicsim.data_structures.State):
    def __init__(self, event_set, facility, servers, population):
        garlicsim.data_structures.State.__init__(self)
        self.event_set = event_set
        self.facility = facility
        self.servers = servers
        self.population = population

    @staticmethod
    def create_root(n_servers=3, population_size=Infinity, mean_arrival=1,
                    mean_service=3):
        
        event_set = events_module.EventSet()
        
        facility = Facility(event_set=event_set)
        
        for i in range(n_servers):
            facility.create_server(mean_service=mean_service)
            
        servers = facility.servers
        
        population = Population(
            event_set=event_set,
            facility=facility,
            size=population_size,
            mean_arrival=mean_arrival
        )
        
        my_state = State(event_set, facility, servers, population)
        
        return my_state

    
    
    def step(self, t=None):
        '''Step function.'''
        # todo good idea: t=None means step to next client. If given int just do
        # many steps. (What with cut last?)
        
        assert t is None # for now
        
        new_state = copy.deepcopy(self, StepCopy())
        time_passed = new_state.event_set.do_next_event()
        
        new_state.clock = self.clock + time_passed
        
        return new_state




            
class Server(object):
    '''
    A server which serves clients in a facility.
    '''
    def __init__(self, event_set, facility, mean_service):
        '''
        Constructor.
        
        `mean_service` is the mean time it takes to service a client.
        '''
        
        self.identity = garlicsim.misc.CrossProcessPersistent()
        
        self.event_set = event_set        
        self.facility = facility
        self.mean_service = mean_service
        
        self.current_client = None
        
        self.finish_service_event = None
        '''
        The event when this server will finish serving the current client.
        '''
        
        self.client_counter = 0
        '''A counter for the number of clients that this server served.'''
    
    def service_client(self, client):
        '''
        Service a client.
        
        The server must be idle.
        '''
        assert self.current_client is None and \
               self.finish_service_event is None
        self.current_client = client
        time_to_next = time_for_next_occurence(self.mean_service)
        self.finish_service_event = \
            self.event_set.create_event(time_to_next, self.finish_client)
        
    def finish_client(self):
        '''Finish serving the currently served client.'''
        assert self.current_client is not None
        self.client_counter += 1
        client = self.current_client 
        self.current_client = None
        self.finish_service_event = None
        self.facility.clients.remove(client)
        self.facility.feed_client(self)
        
        
    def is_busy(self):
        '''Is this server busy serving a client?'''
        return (self.current_client is not None)
    
    def __repr__(self):
        if self.is_busy():
            return '<Server (busy) who served %s clients>' % self.client_counter
        else:
            return '<Server (free) who served %s clients>' % self.client_counter
        

class Client(object):
    '''A client which needs to be served in the facility.'''
    def __init__(self):
        self.identity = garlicsim.misc.CrossProcessPersistent()

        
class Facility(object):
    '''A facility in which there are servers serving clients.'''
    
    def __init__(self, event_set, servers=[], clients=[]):
        
        self.identity = garlicsim.misc.CrossProcessPersistent()
        self.event_set = event_set
        self.servers = servers
        self.clients = clients
        self.waiting_clients = clients[:]
        
    def create_server(self, *args, **kwargs):
        '''Create a new server for this facility.'''
        new_server = Server(self.event_set, self, *args, **kwargs)
        self.servers.append(new_server)
        return new_server
    
    def add_client(self, client):
        '''Add a new client to this facility, to be served by a server.'''
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
        '''Generator that yields servers in the facility that are idle.'''
        inner_generator = (server for server in self.servers
                           if (server.is_busy() is False))
        for idle_server in inner_generator:
            yield idle_server
            
    def feed_client(self, server):
        '''
        Order a server to start servicing the first client in the queue.
        
        The server must be idle.
        '''
        assert server.is_busy() is False
        try:
            client = self.waiting_clients.pop(0)
        except IndexError:
            return None
        server.service_client(client)
    
    def finished_client_count(self):
        '''Return the number of clients that were served by all servers.'''
        return sum((server.client_counter for server in self.servers))
        
    
    def __repr__(self):
        return '''<facility with %s clients, %s of which stand in queue. %s \
clients were served total.>''' % \
            (
                len(self.clients),
                len(self.waiting_clients),
                self.finished_client_count()
            )
        
                    

class Population(object):
    '''A population which generates clients.'''
    def __init__(self, event_set, facility, size=Infinity, mean_arrival=1):
        '''
        Constructor.
        
        `mean_arrival` is the mean time between arrivals.
        '''
        assert size == Infinity
        self.identity = garlicsim.misc.CrossProcessPersistent()
        self.size = size
        self.mean_arrival = mean_arrival
        self.event_set = event_set
        self.facility = facility
        self.next_arrival = None
        self.schedule_next_arrival()
        
    def schedule_next_arrival(self):
        '''Schedule the next arrival of a client from the population.'''
        assert self.next_arrival is None
        time_left = time_for_next_occurence(self.mean_arrival)
        self.next_arrival = self.event_set.create_event(time_left,
                                                        self.make_arrival)
    
    def make_arrival(self):
        '''Create a client and put it into the facility.'''
        client = Client()
        self.facility.add_client(client)
        self.next_arrival = None
        self.schedule_next_arrival()
        return client
    

