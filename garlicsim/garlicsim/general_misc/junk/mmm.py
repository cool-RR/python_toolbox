
from __future__ import with_statement

import multiprocessing
import multiprocessing.queues

class Queue(object):
    def __init__(self, *args, **kwargs):
        self.queue = multiprocessing.Queue()
        self.lock = multiprocessing.Lock()
        
        
    def get(self, *args, **kwargs):
        with self.lock:
            return self.queue.get(*args, **kwargs)
        
    def put(self, *args, **kwargs):
        with self.lock:
            return self.queue.put(*args, **kwargs)
        
    def qsize(self, *args, **kwargs):
        with self.lock:
            return self.queue.qsize(*args, **kwargs)