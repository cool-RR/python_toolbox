
from garlicsim import garlicsim
from . import server

class Facility(object):
    '''A facility in which there are servers serving clients.'''
    
    def __init__(self, event_set, servers=[], clients=[]):
        
        self.identity =\
            garlicsim.general_misc.persistent.CrossProcessPersistent()
        self.event_set = event_set
        self.servers = servers
        self.clients = clients
        self.waiting_clients = clients[:]
        
    def create_server(self, *args, **kwargs):
        '''Create a new server for this facility.'''
        new_server = server.Server(self.event_set, self, *args, **kwargs)
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
        return ('<facility with %s clients, %s of which stand in queue. %s '
                'clients were served total.>''' % \
                (
                    len(self.clients),
                    len(self.waiting_clients),
                    self.finished_client_count()
                )
                )
        
                    

 