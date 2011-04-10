# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `Server` class.

See its documentation for more information.
'''

from garlicsim.general_misc import identities

import garlicsim
from .server import Server


class Facility(identities.HasIdentity):
    '''A facility in which there are servers serving clients.'''
    
    def __init__(self, event_set, servers=[], clients=[]):
        identities.HasIdentity.__init__(self)
        
        self.event_set = event_set
        '''
        An event set for events such as servers finishing or clients arriving.
        '''
        
        self.servers = servers
        '''List of all the servers in the facility.'''
        
        self.clients = clients
        '''
        List of all the clients, both those getting served and those on queue.
        '''
        
        self.waiting_clients = clients[:]
        '''List of all the clients waiting in the queue.'''
        
        
    def create_server(self, mean_service_time):
        '''Create a new server for this facility.'''
        new_server = Server(
            event_set=self.event_set,
            facility=self,
            mean_service_time=mean_service_time
        )
        self.servers.append(new_server)
        return new_server

    
    def add_client(self, client):
        '''Add a new client to this facility, to be served by a server.'''
        self.clients.append(client)
        if not self.waiting_clients: # Queue is empty, no waiting clients
            # If there's an idle server, have it service the new client:
            idle_servers = list(self.idle_servers_generator())
            if idle_servers:
                first_idle_server = idle_servers[0]
                first_idle_server.service_client(client)
            else:
                self.waiting_clients.append(client)
        else: # There are clients awaiting in the queue
            self.waiting_clients.append(client)
            
            
    def idle_servers_generator(self):
        '''Generator that yields servers in the facility that are idle.'''
        for server in self.servers:
            if not server.is_busy():
                yield server
            
            
    def feed_client(self, server):
        '''
        Order a server to start servicing the first client in the queue.
        
        The server must be idle.
        '''
        assert not server.is_busy()
        if self.waiting_clients:
            client = self.waiting_clients.pop(0)
            server.service_client(client)
        
    
    def finished_client_count(self):
        '''Return the number of clients that were served by all servers.'''
        return sum((server.client_counter for server in self.servers))
        
    
    def __repr__(self):
        return ('<facility with %s clients, %s of which stand in queue. %s '
                'clients were served total.>' % \
                (
                    len(self.clients),
                    len(self.waiting_clients),
                    self.finished_client_count()
                )
                )
        
                    

 