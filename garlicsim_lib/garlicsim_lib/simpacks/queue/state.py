# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.
'''
This module defines the `State` class.

See its documentation for more information.
'''

from __future__ import division

from garlicsim.general_misc.infinity import infinity
import garlicsim

from . import events as events_module
from .facility import Facility
from .population import Population


class State(garlicsim.data_structures.State):
    '''World state. A frozen moment in time in the simulation world.'''
    
    def __init__(self, event_set, facility, servers, population):
        garlicsim.data_structures.State.__init__(self)
        
        self.event_set = event_set
        '''Event set for events such as new clients arriving.'''
        	
        self.facility = facility
        '''The facility in which clients wait to be serviced.'''
        
        self.servers = servers
        '''Servers which service the clients.'''
        
        self.population = population
        '''Population from which the clients arrive.'''

        
    @staticmethod
    def create_root(n_servers=3, population_size=infinity, mean_arrival_time=1,
                    mean_service_time=3):
        '''Create a plain and featureless world state.'''
        
        event_set = events_module.EventSet()
        
        facility = Facility(event_set=event_set)
        
        for i in range(n_servers):
            facility.create_server(mean_service_time=mean_service_time)
                    
        population = Population(
            event_set=event_set,
            facility=facility,
            size=population_size,
            mean_arrival_time=mean_arrival_time
        )
        
        return State(
            event_set=event_set,
            facility=facility,
            servers=facility.servers,
            population=population
        )
    
    
    def inplace_step(self):
        '''Modify the state in-place to make it the next moment in time.'''
        
        # todo good idea: t=None means step to next client. If given int just
        # do many steps. (What with cut last?)
        
        time_passed = self.event_set.do_next_event()
        self.clock += time_passed

        