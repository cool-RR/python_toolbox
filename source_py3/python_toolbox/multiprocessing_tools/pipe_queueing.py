# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import multiprocessing

class PipeQueue:
    def __init__(self):
        self.queue = multiprocessing.Queue()
        
    def create_pipe(self):
        master_connection, slave_connection = multiprocessing.Pipe()
        self.queue.put(slave_connection)
        return master_connection
    
    def wait_for_connection(self):
        return self.queue.get()
    
    
        
        
        