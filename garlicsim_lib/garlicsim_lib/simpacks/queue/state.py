# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Core module for `queue` simpack for simulations in Queueing Theory.
'''

from __future__ import division

import Queue
import random
import copy

from garlicsim.general_misc.infinity import infinity
import garlicsim

from . import events as events_module
from .server import Server
from .facility import Facility
from . import math_tools
from . import client


class State(garlicsim.data_structures.State):
    '''
    World state. A frozen moment in time in the simulation world.
    
    '''
    def __init__(self, event_set, facility, servers, population):
        garlicsim.data_structures.State.__init__(self)
        self.event_set = event_set
        self.facility = facility
        self.servers = servers
        self.population = population

    @staticmethod
    def create_root(n_servers=3, population_size=infinity, mean_arrival=1,
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

    
    
    def inplace_step(self): #, t=None):
        '''Inplace step function.'''
        # todo good idea: t=None means step to next client. If given int just
        # do many steps. (What with cut last?)
        
        time_passed = self.event_set.do_next_event()
        self.clock += time_passed




            
class Population(object):
    '''A population which generates clients.'''
    def __init__(self, event_set, facility, size=infinity, mean_arrival=1):
        '''
        Constructor.
        
        `mean_arrival` is the mean time between arrivals.
        '''
        assert size == infinity
        self.identity = \
            garlicsim.general_misc.persistent.CrossProcessPersistent()
        self.size = size
        self.mean_arrival = mean_arrival
        self.event_set = event_set
        self.facility = facility
        self.next_arrival = None
        self.schedule_next_arrival()
        
    def schedule_next_arrival(self):
        '''Schedule the next arrival of a client from the population.'''
        assert self.next_arrival is None
        time_left = math_tools.time_for_next_occurence(self.mean_arrival)
        self.next_arrival = self.event_set.create_event(time_left,
                                                        self.make_arrival)
    
    def make_arrival(self):
        '''Create a client and put it into the facility.'''
        client = client.Client()
        self.facility.add_client(client)
        self.next_arrival = None
        self.schedule_next_arrival()
        return client
    

