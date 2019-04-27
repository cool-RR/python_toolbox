# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import wx

from python_toolbox.temp_value_setting import TempValueSetter


class CursorChanger(TempValueSetter):
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
        TempValueSetter.__init__(self,
                                 (window.GetCursor, window.SetCursor),
                                 self.cursor,
                                 assert_no_fiddling=False)