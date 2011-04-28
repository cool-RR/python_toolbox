# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''

import wx


class CuteWindow(wx.Window):
    
    def add_accelerators(self, accelerators):
        if not getattr(self, '_CuteWindow__initialized', False):
            self.__accelerator_table = None
            self.__accelerators = []
            self.__initialized = True
        
        self.__accelerators += accelerators
        self.__accelerator_table = wx.AcceleratorTable(self.__accelerators)
        self.SetAcceleratorTable(self.__accelerator_table)