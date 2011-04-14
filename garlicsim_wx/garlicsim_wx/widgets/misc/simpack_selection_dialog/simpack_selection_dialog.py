# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `SimpackSelectionDialog` class.

See its documentation for more info.
'''

import os
import sys
import glob
import pkgutil

import wx
import pkg_resources

from garlicsim.general_misc.cmp_tools import underscore_hating_cmp
from garlicsim.general_misc import address_tools
from garlicsim.general_misc import path_tools
from garlicsim.general_misc import import_tools
from garlicsim.general_misc import package_finder
from garlicsim_wx.widgets.general_misc.cute_dialog import CuteDialog
from garlicsim_wx.general_misc import wx_tools

import garlicsim_wx

from . import images as __images_package
images_package = __images_package.__name__

# blocktodo: Don't forget keyboard shortcuts for everything, like back/forward.

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
            self.__init_build()
            
        
    def __init_build(self):
        
        is_mac = (wx.Platform == '__WXGTK__')
        
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
        
        text_ctrl_0 = wx.TextCtrl(self)
        self.flex_grid_sizer.Add(text_ctrl_0,
                                 proportion=1,
                                 flag=wx.EXPAND | wx.ALL,
                                 border=5)
        
        text_ctrl_1 = wx.TextCtrl(self)
        self.flex_grid_sizer.Add(text_ctrl_1,
                                 proportion=1,
                                 flag=wx.EXPAND | wx.ALL,
                                 border=5)
        
        #text_ctrl_2 = wx.TextCtrl(self)
        #self.flex_grid_sizer.Add(text_ctrl_2, 0, wx.EXPAND)
        
        
        #######################################################################
        #######################################################################
        ### Building simpack-navigation buttons: ##############################
        #                                                                     #

        self.big_simpack_navigation_sizer = wx.BoxSizer(wx.VERTICAL)
        self.flex_grid_sizer.Add(self.big_simpack_navigation_sizer,
                                 proportion=0,
                                 flag=wx.EXPAND)
        
        self.add_simpacks_from_a_different_folder = wx.Button(
            self,
            label='&Add simpacks from a different folder...'
        )
        self.big_simpack_navigation_sizer.Add(
            self.add_simpacks_from_a_different_folder,
            proportion=0,
            flag=wx.EXPAND | wx.ALL,
            border=5
        )
        self.Bind(wx.EVT_BUTTON,
                  self.on_add_folder_containing_simpacks_button,
                  self.add_simpacks_from_a_different_folder)
        
        self.small_simpack_navigation_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.big_simpack_navigation_sizer.Add(
            self.small_simpack_navigation_sizer,
            proportion=0,
            flag=wx.EXPAND
        )
        
        ### Building search box: ##############################################
        #                                                                     #
        self.search_sizer = wx.BoxSizer(wx.VERTICAL)
        self.small_simpack_navigation_sizer.Add(
            self.search_sizer,
            proportion=1,
            flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT,
            border=5
        )
        
        self.search_static_text = wx.StaticText(
            self,
            label='S&earch for simpacks:'
        )
        self.search_sizer.Add(
            self.search_static_text,
            proportion=1,
            flag=wx.ALIGN_LEFT | wx.TOP | wx.BOTTOM,
            border=5,
        )
            
        
        # blocktodo: if `wx.SearchCtrl` doesn't give us everything we need, can
        # find something else.
        # blocktodo: not getting enough padding for the search control on Mac
        self.search_ctrl = wx.SearchCtrl(self)
        self.search_ctrl.ShowCancelButton(True)
        self.search_ctrl.SetDescriptiveText('')
        self.search_sizer.Add(
            self.search_ctrl,
            proportion=0,
            flag=wx.EXPAND | wx.TOP | wx.BOTTOM,
            border=5,
        )
        #                                                                     #
        ### Finished building search box. #####################################
        
        ### Building back and forward buttons: ################################
        #                                                                     #
        self.back_button = wx.BitmapButton(
            self,
            bitmap=wx.BitmapFromImage(
                wx.ImageFromStream(
                    pkg_resources.resource_stream(images_package, 'back.png'),
                    wx.BITMAP_TYPE_ANY
                )
            ),
        )
        self.small_simpack_navigation_sizer.Add(
            self.back_button,
            proportion=0,
            flag=wx.ALL | wx.ALIGN_BOTTOM,
            border=5
        )
        
        self.forward_button = wx.BitmapButton(
            self,
            bitmap=wx.BitmapFromImage(
                wx.ImageFromStream(
                    pkg_resources.resource_stream(images_package, 'forward.png'),
                    wx.BITMAP_TYPE_ANY
                )
            ),
        )
        self.small_simpack_navigation_sizer.Add(
            self.forward_button,
            proportion=0,
            flag=wx.ALL | wx.ALIGN_BOTTOM,
            border=5
        )
        #                                                                     #
        ### Finished building back and forward buttons. #######################
        
        if is_mac:
            self.big_simpack_navigation_sizer.AddSpacer(5)
        
        #                                                                     #
        ### Finished building simpack-navigation buttons. #####################
        #######################################################################
        #######################################################################
        
        #text_ctrl_3 = wx.TextCtrl(self)
        #self.flex_grid_sizer.Add(text_ctrl_3, 0, wx.EXPAND)
        
        
        ### Creating Ok/Cancel buttons: #######################################
        #                                                                     #
        self.dialog_button_sizer = wx.StdDialogButtonSizer()
        # blocktodo: make big and spaced like in mockup
        
        self.flex_grid_sizer.Add(self.dialog_button_sizer,
                                 0,
                                 flag=wx.ALIGN_CENTER_HORIZONTAL | \
                                      wx.ALIGN_CENTER_VERTICAL | \
                                      wx.ALL,
                                 border=5)
        
        self.ok_button = wx.Button(self, wx.ID_OK, 'Create &project')
        self.dialog_button_sizer.AddButton(self.ok_button)
        self.ok_button.SetDefault()
        self.dialog_button_sizer.SetAffirmativeButton(self.ok_button)
        self.Bind(wx.EVT_BUTTON, self.on_ok, source=self.ok_button)
        
        self.cancel_button = wx.Button(self, wx.ID_CANCEL, 'Cancel')
        self.dialog_button_sizer.AddButton(self.cancel_button)
        self.Bind(wx.EVT_BUTTON, self.on_cancel, source=self.cancel_button)
        self.dialog_button_sizer.Realize()
        #                                                                     #
        ### Finished creating Ok/Cancel buttons. ##############################
        
        
        self.Layout()
        
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



