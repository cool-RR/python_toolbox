# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `EventHandlerGrokker` class.

See its documentation for more information.
'''

import types

import wx

from garlicsim.general_misc import caching

from .event_codes import get_event_code_of_component, get_event_code_from_name


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
        assert name.startswith('_on_')
        
        self.name = name
        
        self.event_handler_self_taking_function = event_handler_self_taking_function
        
        self.window_type = window_type
        
        
    cleaned_name = caching.CachedProperty(
        lambda self: self.name[4:],
        doc=''' '''
    )

    
    def bind(self, window):
        assert isinstance(window, wx.Window)
        event_handler_bound_method = types.MethodType(    
            self.event_handler_self_taking_function,
            window,
            self.window_type
        )
        component_candidate = getattr(window, self.cleaned_name, None)
        if component_candidate is not None and \
           hasattr(component_candidate, 'GetId'):
            component = component_candidate
            return window.Bind(
                get_event_code_of_component(component),
                event_handler_bound_method, #self.event_handler,
                source=component
            )
        else:
            return window.Bind(
                get_event_code_from_name(self.cleaned_name, self.window_type),
                event_handler_bound_method #self.event_handler,
            )
                
            
        
        
        