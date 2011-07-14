# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `EventHandlerGrokker` class.

See its documentation for more information.
'''

import types

import wx

from garlicsim.general_misc import caching
from garlicsim.general_misc import address_tools

from .event_codes import get_event_codes_of_component, get_event_code_from_name


class EventHandlerGrokker(object):
    '''Wraps an event handling function and figures out what to bind it to.'''
    
    def __init__(self, name, event_handler_self_taking_function, window_type):
        '''
        Construct the `EventHandlerGrokker`.
        
        `name` is the name of the event handling function.
        `event_handler_self_taking_function` is the function itself, as proper
        function. (i.e. taking two arguments `self` and `event`.) `window_type`
        is the class in which that event handler is defined.
        '''
        assert window_type._BindSavvyWindowType__name_parser.match(
            name,
            window_type.__name__
        )
        
        self.name = name
        
        self.event_handler_self_taking_function = \
            event_handler_self_taking_function
        
        self.window_type = window_type
        
        
    parsed_words = caching.CachedProperty(
        lambda self: self.window_type._BindSavvyWindowType__name_parser.parse(
            self.name,
            self.window_type.__name__
        ),
        doc=''' '''
    )

    
    def bind(self, window):
        assert isinstance(window, wx.Window)
        event_handler_bound_method = types.MethodType(    
            self.event_handler_self_taking_function,
            window,
            self.window_type
        )
        if len(self.parsed_words) >= 2:
            closer_window = address_tools.resolve(
                '.'.join(('window',) + self.parsed_words[:-1]),
                namespace={'window': window}
            )
        else:
            closer_window = None
        last_word = self.parsed_words[-1]
        component_candidate = getattr(closer_window or window, last_word, None)
        if component_candidate is not None and \
           hasattr(component_candidate, 'GetId'):
            component = component_candidate
            event_codes = get_event_codes_of_component(component)
            for event_code in event_codes:
                window.Bind(
                    event_code,
                    event_handler_bound_method,
                    source=component
                )
                
        else:
            window.Bind(
                get_event_code_from_name(last_word,
                                         self.window_type),
                event_handler_bound_method,
            )
                
            
        
        
        