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
    
    __depth = caching.CachedProperty(lambda self: 0, doc='''blocktododoc''')
    # blocktodo: should CachedProperty take a non-callable?
    
    depth = property(
        fget=lambda self: self.__depth,
        fset=lambda self, value: setattr(self,
                                         '_ReentrantContextManager__depth',
                                         value)
    )
    #blocktodo: develop ProxyProperty

    
    def __enter__(self):
        if self.__depth == 0:
            self.__enter_return_value = self.reentrant_enter()
        self.__depth += 1
        return self.__enter_return_value
    
    
    def __exit__(self, type_, value, traceback):
        assert self.__depth >= 1
        if self.__depth == 1:
            self.reentrant_exit(type_, value, traceback)
        # todo: if in depth, perhaps should save exception data if it exists
        # and pass to outermost?
        self.__depth -= 1

        
    def reentrant_enter(self):
        ''' '''
        return self
        
    
    def reentrant_exit(self, type_, value, traceback):
        ''' '''
        pass