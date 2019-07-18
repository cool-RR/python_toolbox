# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

import types

import wx

from python_toolbox import caching
from python_toolbox import address_tools

from .event_codes import get_event_codes_of_component, get_event_code_from_name


class EventHandlerGrokker(object):
    '''Wraps an event handling function and figures out what to bind it to.'''

    def __init__(self, name, event_handler_self_taking_function,
                 evt_handler_type):
        '''
        Construct the `EventHandlerGrokker`.

        `name` is the name of the event handling function.
        `event_handler_self_taking_function` is the function itself, as proper
        function. (i.e. taking two arguments `self` and `event`.)
        `evt_handler_type` is the class in which that event handler is defined.
        '''
        assert evt_handler_type._BindSavvyEvtHandlerType__name_parser.match(
            name,
            evt_handler_type.__name__
        )

        self.name = name

        self.event_handler_self_taking_function = \
            event_handler_self_taking_function

        self.evt_handler_type = evt_handler_type


    parsed_words = caching.CachedProperty(
        lambda self: self.evt_handler_type. \
                                   _BindSavvyEvtHandlerType__name_parser.parse(
            self.name,
            self.evt_handler_type.__name__
        ),
        doc=''' '''
    )


    def bind(self, evt_handler):
        assert isinstance(evt_handler, wx.EvtHandler)
        event_handler_bound_method = types.MethodType(
            self.event_handler_self_taking_function,
            evt_handler,
        )
        if len(self.parsed_words) >= 2:
            closer_evt_handler = address_tools.resolve(
                '.'.join(('window',) + self.parsed_words[:-1]),
                namespace={'window': evt_handler}
            )
        else:
            closer_evt_handler = None
        last_word = self.parsed_words[-1]
        component_candidate = getattr(closer_evt_handler or evt_handler,
                                      last_word, None)
        if component_candidate is not None and \
           hasattr(component_candidate, 'GetId'):
            component = component_candidate
            event_codes = get_event_codes_of_component(component)
            for event_code in event_codes:
                evt_handler.Bind(
                    event_code,
                    event_handler_bound_method,
                    source=component
                )

        else:
            evt_handler.Bind(
                get_event_code_from_name(last_word,
                                         self.evt_handler_type),
                event_handler_bound_method,
            )




