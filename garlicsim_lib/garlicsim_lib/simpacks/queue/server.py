# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `Server` class.

See its documentation for more information.
'''

from garlicsim.general_misc import identities
import garlicsim

from . import math_tools


class Server(identities.HasIdentity):
    '''A server which serves clients in a facility.'''
    
    def __init__(self, event_set, facility, mean_service):
        '''
        Constructor.
        
        `mean_service` is the mean time it takes to service a client.
        '''
        identities.HasIdentity.__init__(self)
        
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
        time_to_next = math_tools.time_for_next_occurence(self.mean_service)
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
            return '<Server (busy) who served %s clients>' % \
                   self.client_counter
        else:
            return '<Server (free) who served %s clients>' % \
                   self.client_counter
        

 