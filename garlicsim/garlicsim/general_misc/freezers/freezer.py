# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
'''

from garlicsim.general_misc.third_party import abc

from garlicsim.general_misc import context_managers
from garlicsim.general_misc import proxy_property
from garlicsim.general_misc import caching

from .delegatee_context_manager import DelegateeContextManager


class Freezer(context_managers.DelegatingContextManager):
    
    delegatee_context_manager = caching.CachedProperty(DelegateeContextManager)

        
    frozen = proxy_property.ProxyProperty('delegatee_context_manager.depth')
    
    
    @abc.abstractmethod
    def freeze_handler(self):
        ''' '''
    
    @abc.abstractmethod
    def thaw_handler(self):
        ''' '''