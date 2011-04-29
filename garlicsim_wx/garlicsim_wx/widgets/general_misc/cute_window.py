# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''

import wx

from garlicsim_wx.general_misc import wx_tools
from garlicsim.general_misc import sequence_tools


def _key_dict_to_accelerators(key_dict):
    accelerators = []
    for key, id in key_dict.items():
        if sequence_tools.is_sequence(key):
            0 0 0
        if isinstance(key, int):
            key = wx_tools.Key(key)
        assert isinstance(key, wx_tools.Key)
        (modifiers, key_code) = key.to_accelerator_pair()
        accelerator = (modifiers, key_code, id)
        accelerators.append(accelerator)
    return accelerators

class CuteWindow(wx.Window):
    
    def add_accelerators(self, accelerators):
        if not getattr(self, '_CuteWindow__initialized', False):
            self.__accelerator_table = None
            self.__accelerators = []
            self.__initialized = True
            
        if isinstance(accelerators, dict):
            accelerators = _key_dict_to_accelerators(accelerators)
        
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