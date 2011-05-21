# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines various tools for manipulating windows.'''

import wx

from garlicsim.general_misc.freezers import Freezer


class WindowFreezer(Freezer):
    '''Context manager for freezing the window while the suite executes.'''
    
    def __init__(self, window):
        Freezer.__init__(self)
        assert isinstance(window, wx.Window)
        self.window = window
        
    def freeze_handler(self):
        self.window.Freeze()
        
    def thaw_handler(self):
        self.window.Thaw()