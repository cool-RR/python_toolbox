# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `BindSavvyWindow` class.

See its documentation for more information.
'''

import wx

from garlicsim_wx.general_misc import wx_tools
from garlicsim.general_misc import caching

from .bind_savvy_window_type import BindSavvyWindowType
from . import name_parser


class BindSavvyWindow(wx.Window):
    '''
    Window type that allows binding events automatically by method name.
    
    Use the `.bind_event_handlers` method to bind event handlers by name.
    
    Some of this class's functionality is in its metaclass; see documentation
    of `BindSavvyWindowType`'s methods and attributes for more details.
    '''
    
    __metaclass__ = BindSavvyWindowType
    
    
    _BindSavvyWindowType__name_parser = name_parser.NameParser(
        (name_parser.LowerCase,),
        n_preceding_underscores_possibilities=(1,)
    )
    '''
    The name parser used by this window class for parsing event handlers.
    
    Override this with a different instance of `NameParser` in order to use a
    different naming convention for event handlers.
    '''
    
    def bind_event_handers(self, cls):
        '''
        Look for event-handling methods on `cls` and bind events to them.
        
        For example, a method with a name of `_on_key_down` will be bound to
        `wx.EVT_KEY_DOWN`, while a method with a name of `_on_ok_button` will
        be bound to a `wx.EVT_BUTTON` event sent from `self.ok_button`.
        
        `cls` should usually be the class in whose `__init__` method the
        `bind_event_handers` function is being called.
        '''
        if not isinstance(self, cls):
            raise TypeError('`cls` must be a class that the window is an '
                            'instance of; you gave a `cls` of `%s`, which '
                            '`%s` is not an instance of.' % (cls, self))
        event_handler_grokkers = \
            cls._BindSavvyWindowType__event_handler_grokkers
        for event_handler_grokker in event_handler_grokkers:
            event_handler_grokker.bind(self)
        
        