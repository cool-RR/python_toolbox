# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines various tools for manipulating windows.'''

import wx

from garlicsim.general_misc.context_manager import ContextManager


class WindowFreezer(ContextManager):
    '''Context manager for freezing the window while the suite executes.'''
    def __init__(self, window):
        assert isinstance(window, wx.Window)
        self.window = window
    def __enter__(self):
        self.window.Freeze()
    def __exit__(self, *args, **kwargs):
        self.window.Thaw()