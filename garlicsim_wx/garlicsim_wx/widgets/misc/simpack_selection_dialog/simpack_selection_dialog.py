# Copyright 2009-2011 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
This module defines the `SimpackSelectionDialog` class.

See its documentation for more info.
'''

import os
import sys
import glob
import pkgutil

import wx

from garlicsim.general_misc.cmp_tools import underscore_hating_cmp
from garlicsim.general_misc import address_tools
from garlicsim.general_misc import path_tools
from garlicsim.general_misc import import_tools
from garlicsim.general_misc import package_finder
from garlicsim_wx.widgets.general_misc.cute_dialog import CuteDialog

import garlicsim_wx


class SimpackSelectionDialog(CuteDialog):
    '''Dialog for selecting a simpack when creating a new gui project.'''
    
    def __init__(self, frame):
        CuteDialog.__init__(
            self,
            frame,
            title='Choose simulation package',
            size=(-1, 400)
        )
        
        assert isinstance(frame, garlicsim_wx.Frame)
        self.frame = frame
        
        self.main_v_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.static_text = wx.StaticText(
            self,
            label='Choose a simulation package for your new simulation:'
        )
        self.main_v_sizer.Add(self.static_text, 0, wx.EXPAND | wx.ALL, 10)
        
        self.list_box = wx.ListBox(self)
        self.main_v_sizer.Add(self.list_box, 1, wx.EXPAND | wx.ALL, 10)
        self.list_box.Bind(wx.EVT_LEFT_DCLICK, self.on_ok, self.list_box)
        
        self.add_folder_containing_simpacks_button = wx.Button(
            self,
            label='&Add folder containing simpacks...'
        )
        self.main_v_sizer.Add(self.add_folder_containing_simpacks_button,
                              0,
                              wx.EXPAND | wx.ALL,
                              border=10)            
        self.Bind(wx.EVT_BUTTON,
                  self.on_add_folder_containing_simpacks_button,
                  self.add_folder_containing_simpacks_button)
        
        self.horizontal_line = wx.StaticLine(self)
        self.main_v_sizer.Add(self.horizontal_line,
                              0,
                              wx.EXPAND | wx.ALL,
                              10)
        
        self.dialog_button_sizer = wx.StdDialogButtonSizer()
        
        self.main_v_sizer.Add(self.dialog_button_sizer,
                              0,
                              wx.ALIGN_CENTER_HORIZONTAL | wx.ALL,
                              border=10)
        
        self.ok_button = wx.Button(self, wx.ID_OK, 'Create &project')
        self.dialog_button_sizer.AddButton(self.ok_button)
        self.ok_button.SetDefault()
        self.dialog_button_sizer.SetAffirmativeButton(self.ok_button)
        self.Bind(wx.EVT_BUTTON, self.on_ok, source=self.ok_button)
        
        self.cancel_button = wx.Button(self, wx.ID_CANCEL, 'Cancel')
        self.dialog_button_sizer.AddButton(self.cancel_button)
        self.Bind(wx.EVT_BUTTON, self.on_cancel, source=self.cancel_button)
        self.dialog_button_sizer.Realize()
        
        self.update_simpack_list()
        if self.list_of_simpacks:
            self.list_box.Select(0)
        
        self.SetSizer(self.main_v_sizer)
        self.Layout()
        
        self.list_box.SetFocus()
        
        
    def on_add_folder_containing_simpacks_button(self, event):
        '''Handler for "Add folders containing simpacks" button.'''
        dir_dialog = wx.DirDialog(
            self,
            'Choose folder containing simpacks. Note that you need to choose '
            'the folder that *contains* your simpack, and not the simpack '
            'folder itself.',
            style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST
        )
        try:
            dir_dialog_return_value = dir_dialog.ShowModal()
        finally:
            dir_dialog.Destroy()
            
        if dir_dialog_return_value == wx.ID_OK:
            path = dir_dialog.GetPath()
            if path not in zip(garlicsim_wx.simpack_places)[0]:
                garlicsim_wx.simpack_places.append((path, ''))
                self.update_simpack_list()
            if path not in sys.path:
                sys.path.append(path)
                
        
    def on_ok(self, event):
        '''Handler for "Ok" button.'''
        if self.list_box.GetStringSelection():
            self.EndModal(wx.ID_OK)       
        
        
    def on_cancel(self, event):
        '''Handler for "Cancel" button.'''
        self.EndModal(wx.ID_CANCEL)
        
        
    def update_simpack_list(self):
        '''Update the list of available simpacks.'''
        
        self.list_of_simpacks = []
        
        for path, package_prefix in garlicsim_wx.simpack_places:
            if path not in sys.path:
                sys.path.append(path)
                
            if package_prefix:
                assert package_prefix[-1] == '.'
                package = address_tools.resolve(package_prefix[:-1])
                path_to_search = path_tools.get_path_of_package(package)
            else: # not package_prefix
                path_to_search = path
                
            list_of_simpacks_in_simpack_place = [
                (package_prefix + package_name[1:]) for package_name in
                package_finder.get_packages(path_to_search, self_in_name=False)
            ]
            list_of_simpacks_in_simpack_place.sort(cmp=underscore_hating_cmp)
            
            self.list_of_simpacks += list_of_simpacks_in_simpack_place
            
        self.list_box.SetItems(self.list_of_simpacks)
        

    def get_simpack_selection(self):
        '''Import the selected simpack and return it.'''
        string = self.list_box.GetStringSelection()
        result = import_tools.normal_import(string)
        return result



