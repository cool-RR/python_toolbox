# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines various tools for manipulating windows.'''

import wx

from garlicsim.general_misc.context_managers import ReentrantContextManager


class WindowFreezer(ReentrantContextManager):
    '''Context manager for freezing the window while the suite executes.'''
    
    def __init__(self, window):
        assert isinstance(window, wx.Window)
        self.window = window
        
    def reentrant_enter(self):
        self.window.Freeze()
        
    def reentrant_exit(self, type_, value, traceback):
        self.window.Thaw()