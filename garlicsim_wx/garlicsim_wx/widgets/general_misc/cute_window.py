# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''

import wx

from garlicsim.general_misc import context_manager
from garlicsim.general_misc import caching

class AcceleratorTableFreezer(context_manager.ContextManager):
    # probably acrhive this shit in a branch, probably not needed
    def __init__(self, cute_window):
        self.cute_window = cute_window
        assert isinstance(self.cute_window, CuteWindow)
        self.frozen = 0
        
    def __enter__(self):
        self.frozen += 1
        
    def __exit__(self, exc_type, exc_value, traceback):
        self.frozen -= 1
        if self.frozen == 0:
            self.cute_window._CuteWindow__build_and_set_accelerator_table()
        

class CuteWindow(wx.Window):
    
    accelerator_table_freezer = caching.CachedProperty(AcceleratorTableFreezer)
    
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
        
        if not self.accelerator_table_freezer.frozen:
            self.__build_and_set_accelerator_table()
        
        
    def __build_and_set_accelerator_table(self):
        self.__accelerator_table = wx.AcceleratorTable(self.__accelerators)
        self.SetAcceleratorTable(self.__accelerator_table)