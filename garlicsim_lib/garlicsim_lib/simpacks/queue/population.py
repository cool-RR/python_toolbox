# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `Population` class.

See its documentation for more information.
'''

from garlicsim.general_misc.infinity import infinity
from garlicsim.general_misc import identities
import garlicsim

from . import math_tools

from .client import Client


class Population(identities.HasIdentity):
    '''A population which generates clients.'''
    def __init__(self, event_set, facility, size=infinity, mean_arrival_time=1):
        '''
        Constructor.
        
        `mean_arrival_time` is the mean time between arrivals.
        '''
        identities.HasIdentity.__init__(self)
        if not (size == infinity):
            raise NotImplementedError
        
        self.size = size
        '''
        The size of the population.
        
        If it's finite, then when there are plenty of clients in the facility
        new clients are less likely to arrive, because there are less potential
        clients available.
        '''
        
        self.mean_arrival_time = mean_arrival_time
        '''The mean time between arrivals of clients.'''
        
        self.event_set = event_set
        '''Event set for events such as new clients arriving.'''
        
        self.facility = facility
        '''The facility in which clients are served.'''
        
        self.next_arrival = None
        '''The event of the next arrival.'''
        
        self.schedule_next_arrival()
        
        
    def schedule_next_arrival(self):
        '''Schedule the next arrival of a client from the population.'''
        assert self.next_arrival is None
        self.next_arrival = self.event_set.create_event(
            math_tools.time_for_next_occurence(self.mean_arrival_time),
            self.make_arrival
        )
    
        
    def make_arrival(self):
        '''Create a client and put it into the facility.'''
        client = Client()
        self.facility.add_client(client)
        self.next_arrival = None
        self.schedule_next_arrival()
        return client

