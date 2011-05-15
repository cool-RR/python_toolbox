# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `CursorChanger` class.

See its documentation for more information.
'''

import wx

from garlicsim.general_misc.context_manager import ContextManager



class CursorChanger(ContextManager):
    '''Context manager for showing specified cursor while suite executes.'''
    def __init__(self, window, cursor):
        '''
        Construct the `CursorChanger`.
        
        `cursor` may be either a `wx.Cursor` object or a constant like
        `wx.CURSOR_BULLSEYE`.
        '''
        assert isinstance(window, wx.Window)
        self.window = window
        self.cursor = cursor if isinstance(cursor, wx.Cursor) \
            else wx.StockCursor(cursor)
        self.old_cursor = window.GetCursor()
    def __enter__(self):
        self.window.SetCursor(self.cursor)
    def __exit__(self, *args, **kwargs):
        self.window.SetCursor(self.old_cursor)