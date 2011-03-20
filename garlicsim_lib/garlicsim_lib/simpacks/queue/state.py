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

from . import math_tools
from . import events as events_module
from .server import Server
from .facility import Facility
from .client import Client
from .population import Population


class State(garlicsim.data_structures.State):
    '''World state. A frozen moment in time in the simulation world.'''
    def __init__(self, event_set, facility, servers, population):
        garlicsim.data_structures.State.__init__(self)
        self.event_set = event_set
        self.facility = facility
        self.servers = servers
        self.population = population

    @staticmethod
    def create_root(n_servers=3, population_size=infinity, mean_arrival=1,
                    mean_service_time=3):
        
        event_set = events_module.EventSet()
        
        facility = Facility(event_set=event_set)
        
        for i in range(n_servers):
            facility.create_server(mean_service_time=mean_service_time)
            
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




            
    

