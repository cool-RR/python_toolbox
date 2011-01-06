# Copyright 2009-2011 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
This module defines the `SimpackSelectionDialog` class.

See its documentation for more info.
'''

import os
import glob
import pkgutil

import wx

from garlicsim.general_misc.cmp_tools import underscore_hating_cmp
from garlicsim.general_misc import import_tools
from garlicsim_wx.widgets.general_misc.cute_dialog import CuteDialog


class SimpackSelectionDialog(CuteDialog):
    '''Dialog for selecting a simpack when creating a new gui project.'''
    
    def __init__(self, parent):
        self.make_simpack_list()
        CuteDialog.__init__(
            self,
            parent,
            'Choose simulation package',
        )
        
        self.main_v_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.static_text = wx.StaticText(
            self,
            label='Choose a simulation package for your new simulation:'
        )
        self.main_v_sizer.Add(self.static_text, 0, wx.EXPAND)
        
        self.list_box = wx.ListBox(self, self.list_of_simpacks)
        self.main_v_sizer.Add(self.list_box, 0, wx.EXPAND)
        
        self.horizontal_line_1 = wx.StaticLine(self)
        self.main_v_sizer.Add(self.horizontal_line_1, 0, wx.EXPAND)
        
        self.add_folder_containing_simpacks_button = wx.Button(
            self,
            label='Add folder containing simpacks...'
        )
        self.main_v_sizer.Add(self.add_folder_containing_simpacks_button,
                              0,
                              wx.EXPAND)            
        self.Bind(wx.EVT_BUTTON,
                  self.on_add_folder_containing_simpacks_button,
                  self.add_folder_containing_simpacks_button)
        
        self.horizontal_line_2 = wx.StaticLine(self)
        self.main_v_sizer.Add(self.horizontal_line_2, 0, wx.EXPAND)
        
        self.dialog_button_sizer = wx.StdDialogButtonSizer()
        
        self.main_v_sizer.Add(self.dialog_button_sizer, 0,
                              wx.ALIGN_CENTER | wx.ALL, border=10)
        
        
        self.dialog_button_sizer = wx.StdDialogButtonSizer()
        
        self.main_v_sizer.Add(self.dialog_button_sizer, 0,
                              wx.ALIGN_CENTER | wx.ALL, border=10)
        
        self.ok_button = wx.Button(self, wx.ID_OK, 'Create project')
        self.dialog_button_sizer.AddButton(self.ok_button)
        self.ok_button.SetDefault()
        self.dialog_button_sizer.SetAffirmativeButton(self.ok_button)
        self.Bind(wx.EVT_BUTTON, self.on_ok, source=self.ok_button)
        
        self.cancel_button = wx.Button(self, wx.ID_CANCEL, 'Cancel')
        self.dialog_button_sizer.AddButton(self.cancel_button)
        self.Bind(wx.EVT_BUTTON, self.on_cancel, source=self.cancel_button)
        self.dialog_button_sizer.Realize()
        

        
    def on_add_folder_containing_simpacks_button(self, event):
        wx.fold
        
        
    def on_ok(self, event):
        self.EndModal(wx.ID_OK)
        
    def make_simpack_list(self):
        '''Make a list of available simpacks.'''
        import garlicsim_lib.simpacks as simpacks
        self.list_of_simpacks = [
            module_name for (importer, module_name, is_package)
            in pkgutil.iter_modules(simpacks.__path__)
        ]
        self.list_of_simpacks.sort(cmp=underscore_hating_cmp)
        

    def get_simpack_selection(self):
        '''Import the selected simpack and return it.'''
        string = self.GetStringSelection()
        result = import_tools.normal_import('garlicsim_lib.simpacks.' + string)
        return result



