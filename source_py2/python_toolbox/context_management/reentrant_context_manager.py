# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines the `ReentrantContextManager` class.

See its documentation for more information.
'''

import abc

from python_toolbox import caching
from python_toolbox.misc_tools import ProxyProperty

from .context_manager import ContextManager


class ReentrantContextManager(ContextManager):
    '''
    A context manager which can be entered several times before it's exited.
    
    Subclasses should override `reentrant_enter` and `reentrant_exit`, which
    are analogues to `__enter__` and `__exit__`, except they are called only on
    the outermost suite. In other words: When you enter the reentrant context
    manager for the first time, `reentrant_enter` is called. If you enter it
    for a second time, nothing is called. Now `.depth == 2`. Exit it now,
    nothing is called. Exit it again, and `reentrant_exit` is called.
    
    Note: The value returned by `reentrant_enter` will be returned by all the
    no-op `__enter__` actions contained in the outermost suite.
    '''
    
    depth = caching.CachedProperty(
        0,
        doc='''
            The number of nested suites that entered this context manager.
            
            When the context manager is completely unused, it's `0`. When it's
            first used, it becomes `1`. When its entered again, it becomes `2`.
            If it is then exited, it returns to `1`, etc.
            '''
    )

    
    def __enter__(self):
        '''Enter the context manager.'''
        if self.depth == 0:
            self.__last_reentrant_enter_return_value = self.reentrant_enter()
        self.depth += 1
        return self.__last_reentrant_enter_return_value
    
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        '''Exit the context manager.'''
        assert self.depth >= 1
        if self.depth == 1:
            # Saving `reentrant_exit`'s return value, since it might be
            # signalling an exception swallowing:
            return_value = self.reentrant_exit(exc_type,
                                               exc_value,
                                               exc_traceback)
        else:
            return_value = None
        self.depth -= 1
        return return_value

        
    def reentrant_enter(self):
        '''Function that gets called when entering the outermost suite.'''
        return self
        
    
    def reentrant_exit(self, exc_type, exc_value, exc_traceback):
        '''Function that gets called when exiting the outermost suite.'''
        pass
    