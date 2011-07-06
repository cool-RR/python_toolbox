# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `BindSavvyWindowType` metaclass.

See documentation of `BindSavvyWindow` for more information.
'''

import wx

from garlicsim.general_misc import caching
from garlicsim.general_misc import dict_tools

from .event_handler_grokker import EventHandlerGrokker


class BindSavvyWindowType(type):
    '''
    Metaclass for the `BindSavvyWindow` class.
    
    See documentation of `BindSavvyWindow` for more information.
    '''
    
    event_modules = []
    '''
    Modules in which events of the form `EVT_WHATEVER` will be searched.
    
    You may override this with either a module or a list of modules, and they
    will be searched when encountering an event handler function with a
    corresponding name. (e.g. `_on_whatever`.)
    '''
    
    @property
    @caching.cache()
    def _BindSavvyWindowType__event_handler_grokkers(cls):
        '''
        The `EventHandlerGrokker` objects for this window.
        
        Each grokker corresponds to an event handler function and its
        responsibilty is to figure out the correct event to handle based on the
        function's name. See documentation of `EventHandlerGrokker` for more
        information.
        '''
        
        names_to_event_handlers = dict_tools.filter_items(
            vars(cls),
            lambda name, value:
                cls._BindSavvyWindowType__name_parser.match(name, cls) and
                callable(value) and
                getattr(value, '_BindSavvyWindowType__dont_bind_automatically',
                        None) is not True
        )
        '''Dict mapping names to event handling functions.'''
        
        return [EventHandlerGrokker(name, value, cls) for (name, value) in
                names_to_event_handlers.items()]
    
    
    @staticmethod
    def dont_bind_automatically(function):
        '''
        Decorate a method to not be bound automatically as an event handler.
        '''
        function._BindSavvyWindowType__dont_bind_automatically = True
        return function