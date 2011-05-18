# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
'''

from garlicsim.general_misc import context_managers
from garlicsim.general_misc import proxy_property


class Freezer(context_managers.ReentrantContextManager):
    
    def __init__(self, thing):
        self.thing = thing

        
    frozen = proxy_property.ProxyProperty('_ReentrantContextManager__depth')
    

    def reentrant_enter(self):
        ''' '''
        return self.__freezer_property._freeze_handler(self.thing)
    
    
    def reentrant_exit(self, type_, value, traceback):
        ''' '''
        return self.__freezer_property._thaw_handler(self.thing)
    
# del Freezer.depth # blocktodo: How do I do this?