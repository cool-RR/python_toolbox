# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''

import wx

from garlicsim_wx.general_misc import wx_tools
from garlicsim.general_misc import caching

from .bind_savvy_window_type import BindSavvyWindowType


class BindSavvyWindow(wx.Window):
    '''
    '''
    
    __metaclass__ = BindSavvyWindowType
    
    
    def find_and_bind_event_handers(self, cls): #blocktodo: move to base class?
        if not isinstance(self, cls):
            raise Exception('blocktododoc')
        event_handler_grokkers = cls._CuteWindowType__event_handler_grokkers
        for event_handler_grokker in event_handler_grokkers:
            event_handler_grokker.bind(self)
        
        