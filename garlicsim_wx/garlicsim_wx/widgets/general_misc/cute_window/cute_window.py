# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''

import wx

from garlicsim_wx.general_misc import wx_tools
from garlicsim.general_misc import caching
from garlicsim.general_misc.context_manager import ContextManager

from .accelerator_savvy_window import AcceleratorSavvyWindow



class CuteWindow(AcceleratorSavvyWindow, wx.Window):
    '''
    
    This class doesn't require calling its `__init__` when subclassing. (i.e.,
    you *may* call its `__init__` if you want, but it will do the same as
    calling `wx.Window.__init__`.)
    '''
    
    freezer = caching.CachedProperty(
        wx_tools.window_tools.WindowFreezer,
        '''Context manager for freezing the window while the suite executes.'''
    )
    
    def create_cursor_changer(cursor):
        '''
        
        `cursor` may be either a `wx.Cursor` object or a constant like
        `wx.CURSOR_BULLSEYE`.
        '''
        return wx_tools.cursors.CursorChanger(self, cursor)
    
    def set_good_background_color(self):
        self.SetBackgroundColour(wx_tools.colors.get_background_color())