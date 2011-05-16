# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `ReentrantContextManager` class.

See its documentation for more information.
'''

from garlicsim.general_misc.third_party import abc

from garlicsim.general_misc import caching

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
            if (type_ is value is traceback is None):
                self.reentrant_exit()
            else:
                self.reentrant_exit(type_, value, traceback)
        self.depth -= 1

        
    @abc.abstractmethod
    def reentrant_enter(self):
        ''' '''
        
    
    @abc.abstractmethod
    def reentrant_exit(self, type_, value, traceback):
        ''' '''