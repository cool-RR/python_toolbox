# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `SimpackSelectionDialog` class.

See its documentation for more info.
'''

from __future__ import with_statement

import os
import sys
import glob
import pkgutil

import wx
import pkg_resources

from garlicsim.general_misc import comparison_tools
from garlicsim.general_misc import address_tools
from garlicsim.general_misc import path_tools
from garlicsim.general_misc import import_tools
from garlicsim.general_misc import package_finder
from garlicsim_wx.widgets.general_misc.cute_dialog import CuteDialog
from garlicsim_wx.general_misc import wx_tools

import garlicsim_wx


# blocktodo: Go over all methods here, ensure they're relevant.

MAC_BOTTOM_SPACING_SIZE = 10

class SimpackSelectionDialog(CuteDialog):
    '''Dialog for selecting a simpack when creating a new gui project.'''

    
    def __init__(self, frame):
        CuteDialog.__init__(
            self,
            frame,
            title='Choose simulation package',
            size=(950, 550)
        )
        
        assert isinstance(frame, garlicsim_wx.Frame)
        self.frame = frame
        
        with wx_tools.WindowFreezer(self):
            with self.accelerator_table_freezer:
                self.__init_build()
            
        
    def __init_build(self):
        
        ### Setting up flex-grid-sizer: #######################################
        #                                                                     #
        self.flex_grid_sizer = wx.FlexGridSizer(rows=2, cols=2,
                                                hgap=16, vgap=0)
        
        self.SetSizer(self.flex_grid_sizer)
        
        self.flex_grid_sizer.AddGrowableRow(0, 1)
        
        self.flex_grid_sizer.AddGrowableCol(0, 2)
        self.flex_grid_sizer.AddGrowableCol(1, 3)
        #                                                                     #
        ### Finished setting up flex-grid-sizer. ##############################
        
        ### Building simpack tree: ############################################
        #                                                                     #
        
        self.simpack_tree_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.flex_grid_sizer.Add(self.simpack_tree_sizer,
                                 proportion=1,
                                 flag=wx.EXPAND | wx.ALL,
                                 border=5)
        
        self.choose_a_simpack_static_text = wx.StaticText(
            self,
            label='Choose a &simpack:'
        )
        self.simpack_tree_sizer.Add(
            self.choose_a_simpack_static_text,
            proportion=0,
            flag=wx.ALIGN_LEFT | wx.BOTTOM,
            border=5,
        )
        
        self.simpack_tree = SimpackTree(self)
        
        self.simpack_tree_sizer.Add(
            self.simpack_tree,
            proportion=1,
            flag=wx.EXPAND | wx.TOP,
            border=0,
        )
        #                                                                     #
        ### Finished building simpack tree. ###################################
        
        ### Building simpack info panel: ######################################
        #                                                                     #
        text_ctrl_1 = wx.TextCtrl(self)
        self.flex_grid_sizer.Add(text_ctrl_1,
                                 proportion=1,
                                 flag=wx.EXPAND | wx.ALL,
                                 border=5)
        #                                                                     #
        ### Finished building simpack info panel. #############################
        
        
        ### Building simpack-navigation panel: ################################
        #                                                                     #
        self.navigation_panel = NavigationPanel(self)
        self.flex_grid_sizer.Add(self.navigation_panel,
                                 proportion=0,
                                 flag=wx.EXPAND)
        #                                                                     #
        ### Finished building simpack-navigation panel. #######################
        
        
        ### Creating Ok/Cancel buttons: #######################################
        #                                                                     #
        self.dialog_button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.flex_grid_sizer.Add(self.dialog_button_sizer,
                                 0,
                                 flag=wx.EXPAND | wx.ALL,
                                 border=5)
        
        self.create_project_button = wx.Button(self, wx.ID_OK,
                                               'Create &project')
        self.create_project_button.SetDefault()
        self.Bind(wx.EVT_BUTTON, self.on_create_project,
                  source=self.create_project_button)
        
        self.cancel_button = wx.Button(self, wx.ID_CANCEL, 'Cancel')
        self.Bind(wx.EVT_BUTTON, self.on_cancel, source=self.cancel_button)
        
        if wx_tools.is_win:
            first_button = self.create_project_button
            second_button = self.cancel_button
        else: # Mac or Linux
            first_button = self.cancel_button
            second_button = self.create_project_button
        
        self.dialog_button_sizer.AddStretchSpacer(prop=2)
        self.dialog_button_sizer.Add(first_button,
                                     proportion=0,
                                     flag=wx.ALIGN_CENTER_VERTICAL)
        self.dialog_button_sizer.AddStretchSpacer(prop=1)
        self.dialog_button_sizer.Add(second_button,
                                     proportion=0,
                                     flag=wx.ALIGN_CENTER_VERTICAL)
        self.dialog_button_sizer.AddStretchSpacer(prop=2)
        
        #                                                                     #
        ### Finished creating Ok/Cancel buttons. ##############################
        
        if wx_tools.is_mac:
            self.dialog_button_sizer.AddSpacer(
                MAC_BOTTOM_SPACING_SIZE
            )
        
        
        self.Layout()
        self.simpack_tree.SetFocus()
        
        #######################################################################
        
        refresh_id = wx.NewId()
        self.Bind(wx.EVT_MENU, self._on_refresh, id=refresh_id)
        self.add_accelerators(
            [
                (wx.ACCEL_NORMAL, wx.WXK_F5, refresh_id)
            ]
        )
        
        '''
        
        self.main_v_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.static_text = wx.StaticText(
            self,
            label='Choose a simulation package for your new simulation:'
        )
        self.main_v_sizer.Add(self.static_text, 0, wx.EXPAND | wx.ALL, 10)
        
        self.list_box = wx.ListBox(self)
        self.main_v_sizer.Add(self.list_box, 1, wx.EXPAND | wx.ALL, 10)
        self.list_box.Bind(wx.EVT_LEFT_DCLICK, self.on_ok, self.list_box)
        
        
        
        self.horizontal_line = wx.StaticLine(self)
        self.main_v_sizer.Add(self.horizontal_line,
                              0,
                              wx.EXPAND | wx.ALL,
                              10)
        
        
        
        self.update_simpack_list()
        if self.list_of_simpacks:
            self.list_box.Select(0)
        
        self.SetSizer(self.main_v_sizer)
        self.Layout()
        
        self.list_box.SetFocus()
        '''
        
        
    def on_add_folder_containing_simpacks_button(self, event):
        '''Handler for "Add folders containing simpacks" button.'''
        dir_dialog = wx.DirDialog(
            self,
            'Choose the folder that *contains* your simpack(s), not the '
            'simpack folder itself.',
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
                
        
    def on_create_project(self, event):
        '''Handler for "Ok" button.'''
        if self.list_box.GetStringSelection():
            self.EndModal(wx.ID_OK)       
        
        
    def on_cancel(self, event):
        '''Handler for "Cancel" button.'''
        self.EndModal(wx.ID_CANCEL)
        
        
    """
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
            list_of_simpacks_in_simpack_place.sort(
                key=comparison_tools.underscore_hating_key
            )
            
            self.list_of_simpacks += list_of_simpacks_in_simpack_place
            
        self.list_box.SetItems(self.list_of_simpacks)
    """    

    def get_simpack_selection(self):
        '''Import the selected simpack and return it.'''
        string = self.list_box.GetStringSelection()
        result = import_tools.normal_import(string)
        return result
    
    def _on_refresh(self, event):
        wx.lib.dialogs.messageDialog(self, 'Refresh')


from .navigation_panel import NavigationPanel
from .simpack_tree import SimpackTree
