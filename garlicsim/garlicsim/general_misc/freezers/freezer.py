# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
'''

from garlicsim.general_misc.third_party import abc

from garlicsim.general_misc import context_managers
from garlicsim.general_misc import proxy_property
from garlicsim.general_misc import caching

from .inner_context_manager import InnerContextManager


class Freezer(context_managers.DelegatingContextManager):
    
    delegatee_context_manager = caching.CachedProperty(InnerContextManager)

        
    frozen = proxy_property.ProxyProperty('inner_context_manager.depth')
    
    
    @abc.abstractmethod
    def freeze_handler(self):
        ''' '''
    
    @abc.abstractmethod
    def thaw_handler(self):
        ''' '''