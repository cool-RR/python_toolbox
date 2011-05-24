# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''

from garlicsim.general_misc.third_party import abc

from garlicsim.general_misc import proxy_property

from .context_manager import ContextManager


class DelegatingContextManager(ContextManager):
    
    delegatee_context_manager = abc.abstractproperty()
    
    __enter__ = proxy_property.ProxyProperty('inner_context_manager.__enter__')
    __exit__ = proxy_property.ProxyProperty('inner_context_manager.__exit__')