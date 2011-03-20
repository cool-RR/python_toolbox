# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `Population` class.

See its documentation for more information.
'''

from garlicsim.general_misc.infinity import infinity
import garlicsim

from . import math_tools

from .client import Client


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
        client = Client()
        self.facility.add_client(client)
        self.next_arrival = None
        self.schedule_next_arrival()
        return client

