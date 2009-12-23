# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
See documentation of class ReadWriteLock defined in this module.
'''

import original_read_write_lock

__all__ = ["ReadWriteLock"]

class ContextManager(object):
    def __init__(self, lock, acquire_func):
        self.lock = lock
        self.acquire_func = acquire_func
    def __enter__(self, *args, **kwargs):
        self.acquire_func()
    def __exit__(self, *args, **kwargs):
        self.lock.release()

class ReadWriteLock(original_read_write_lock.ReadWriteLock):
    '''
    A ReadWriteLock subclassed from a different ReadWriteLock class defined
    in the module original_read_write_lock.py, (See the documentation of the
    original class for more details.)
    
    This subclass adds two context managers, one for reading and one for
    writing.
    
    Usage:
    
    lock = ReadWriteLock()
    with lock.read:
        pass #perform read operations here
    with lock.write:
        pass #perform write operations here
    '''
    # todo: rename from acquireRead style to acquire_read style
    def __init__(self, *args, **kwargs):
        original_read_write_lock.ReadWriteLock.__init__(self, *args, **kwargs)
        self.read = ContextManager(self, self.acquireRead)
        self.write = ContextManager(self, self.acquireWrite)