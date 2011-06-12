# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''

import wx

from garlicsim.general_misc import caching
from garlicsim.general_misc import dict_tools

from .event_handler_grokker import EventHandlerGrokker

# blocktododoc: make decorator for "ignore this method"
class BindSavvyWindowType(type):
    
    event_modules = []
    
    @property
    @caching.cache()
    def _BindSavvyWindowType__event_handler_grokkers(cls):
        
        names_to_event_handlers = dict_tools.filter_items(
            vars(cls),
            lambda name, value: name.startswith('_on_') and callable(value)
        )
        
        return [EventHandlerGrokker(name, value, cls) for (name, value) in
                names_to_event_handlers.items()]