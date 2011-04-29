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
        
        for accelerator in accelerators:
            modifiers, key, id = accelerator
            for existing_accelerator in self.__accelerators:
                existing_modifiers, existing_key, existing_id = \
                    existing_accelerator
                if (modifiers, key) == (existing_modifiers, existing_key):
                    self.__accelerators.remove(existing_accelerator)
            self.__accelerators.append(accelerator)
         
        self.__build_and_set_accelerator_table()
        
        
    def __build_and_set_accelerator_table(self):
        self.__accelerator_table = wx.AcceleratorTable(self.__accelerators)
        self.SetAcceleratorTable(self.__accelerator_table)