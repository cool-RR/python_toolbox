# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `ReentrantContextManager` class.

See its documentation for more information.
'''

from garlicsim.general_misc.third_party import abc

from garlicsim.general_misc import caching
from garlicsim.general_misc.proxy_property import ProxyProperty

from .context_manager import ContextManager


class ReentrantContextManager(ContextManager):
    ''' '''
    
    depth = caching.CachedProperty(lambda self: 0, doc='''blocktododoc''')
    # blocktodo: should CachedProperty take a non-callable?

    
    def __enter__(self):
        if self.depth == 0:
            self.__enter_return_value = self.reentrant_enter()
        self.depth += 1
        return self.__enter_return_value
    
    
    def __exit__(self, type_, value, traceback):
        assert self.depth >= 1
        if self.depth == 1:
            self.reentrant_exit(type_, value, traceback)
        # todo: if in depth, perhaps should save exception data if it exists
        # and pass to outermost?
        self.depth -= 1

        
    def reentrant_enter(self):
        ''' '''
        return self
        
    
    def reentrant_exit(self, type_, value, traceback):
        ''' '''
        pass