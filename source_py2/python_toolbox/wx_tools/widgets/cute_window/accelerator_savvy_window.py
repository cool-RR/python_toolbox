# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

import collections

import wx

from python_toolbox import sequence_tools
from python_toolbox import wx_tools


def _key_dict_to_accelerators(key_dict):
    '''
    Convert a dict mapping keys to ids to a list of accelerators.
    
    The values of `key_dict` are wxPython IDs. The keys may be either:
    
      - `Key` instances.
      - Key-codes given as `int`s.
      - Tuples of `Key` instances and/or key-codes given as `int`s.

    Example:
    
        _key_dict_to_accelerators(
            {Key(ord('Q')): quit_id,
             (Key(ord('R'), cmd=True),
              Key(wx.WXK_F5)): refresh_id,
             wx.WXK_F1: help_id}
        ) == [
            (wx.ACCEL_NORMAL, ord('Q'), quit_id),
            (wx.ACCEL_CMD, ord('R'), refresh_id),
            (wx.ACCEL_NORMAL, ord('Q'), refresh_id),
            (wx.ACCEL_NORMAL, wx.WXK_F1, help_id),
        ]
    
    '''
    
    accelerators = []
    
    original_key_dict = key_dict
    key_dict = {}
    
    ### Breaking down key tuples to individual entries: #######################
    #                                                                         #
    for key, id in original_key_dict.items():
        if isinstance(key, collections.Sequence):
            key_sequence = key
            for actual_key in key_sequence:
                key_dict[actual_key] = id
        else:
            key_dict[key] = id
    #                                                                         #
    ### Finished breaking down key tuples to individual entries. ##############
    
    for key, id in key_dict.items():
        if isinstance(key, int):
            key = wx_tools.keyboard.Key(key)
        assert isinstance(key, wx_tools.keyboard.Key)
        (modifiers, key_code) = key.to_accelerator_pair()
        accelerator = (modifiers, key_code, id)
        accelerators.append(accelerator)
    return accelerators


class AcceleratorSavvyWindow(wx.Window):
    
    def add_accelerators(self, accelerators):
        '''
        Add accelerators to the window.
        
        There are two formats for adding accelerators. One is the old-fashioned
        list of tuples, like this:

            cute_window.add_accelerators(
                [
                    (wx.ACCEL_NORMAL, ord('Q'), quit_id),
                    (wx.ACCEL_CMD, ord('R'), refresh_id),
                    (wx.ACCEL_NORMAL, ord('Q'), refresh_id),
                    (wx.ACCEL_NORMAL, wx.WXK_F1, help_id),
               ]
            )
        
        Another is to use a dictionary. The values of the dictionary should be
        wxPython IDs. The keys may be either:
    
         - `Key` instances.
         - Key-codes given as `int`s.
         - Tuples of `Key` instances and/or key-codes given as `int`s.
   
       Here's an example of using a key dictionary that gives an identical
       accelerator table as the previous example which used a list of tuples:
       
           cute_window.add_accelerators(
               {Key(ord('Q')): quit_id,
                (Key(ord('R'), cmd=True),
                 Key(wx.WXK_F5)): refresh_id,
                wx.WXK_F1: help_id}
           )
           
        '''
        if not getattr(self, '_AcceleratorSavvyWindow__initialized', False):
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