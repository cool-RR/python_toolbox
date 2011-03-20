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
    
    def __init__(self, event_set, facility, mean_service_time):
        '''
        Constructor.
        
        `mean_service_time` is the mean time it takes to service a client.
        '''
        identities.HasIdentity.__init__(self)
        
        self.event_set = event_set
        '''Event set for events such as the end of a client's service.'''
        
        self.facility = facility
        '''The facility in which clients are served.'''
        
        self.mean_service_time = mean_service_time
        '''The mean time it takes the server to service a client.'''
        
        self.current_client = None
        '''The current client being serviced by this server.'''
        
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
        self.finish_service_event = self.event_set.create_event(
            math_tools.time_for_next_occurence(self.mean_service_time),
            self.finish_client
        )
        
        
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
        return '<Server (%s) who served %s clients>' % (
            'busy' if self.is_busy() else 'free',
            self.client_counter
        )
        

 