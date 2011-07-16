# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `SimpackSelectionDialog` class.

See its documentation for more info.
'''

from __future__ import with_statement

import wx

from garlicsim_wx.general_misc.cute_timer import CuteTimer
from garlicsim_wx.widgets.general_misc.cute_panel import CutePanel
from garlicsim_wx.widgets.general_misc.cute_dialog import CuteDialog
from garlicsim_wx.widgets.general_misc.cute_hidden_button import \
                                                               CuteHiddenButton
from garlicsim_wx.general_misc import wx_tools

import garlicsim_wx

from .simpack_info_panel import SimpackInfoPanel


# blocktodo: Don't forget tooltips here wherever possible
# blocktodo: On Ubuntu when I pressed X it didn't exit the dialog.


MAC_BOTTOM_SPACING_SIZE = 8


class SimpackSelectionDialog(CuteDialog):
    '''Dialog for selecting a simpack when creating a new gui project.'''
    
    def __init__(self, frame):
        CuteDialog.__init__(
            self,
            frame,
            title='Choose simulation package',
            size=(1000, 550)
        )
        
        assert isinstance(frame, garlicsim_wx.Frame)
        self.frame = frame
        
        self.simpack = None
        self.simpack_metadata = None
        
        
        with self.freezer:
            self.__init_build()
            
            self.simpack_tree.reload_tree()
            self.simpack_tree.ExpandAll()
            self.simpack_tree.ensure_simpack_selected()
            
        
    def __init_build(self):
        
        ### Setting up flex-grid-sizer: #######################################
        #                                                                     #
        self.flex_grid_sizer = wx.FlexGridSizer(rows=2, cols=2,
                                                hgap=8, vgap=0)
        
        self.SetSizer(self.flex_grid_sizer)
        
        self.flex_grid_sizer.AddGrowableRow(0, 1)
        
        self.flex_grid_sizer.AddGrowableCol(0, 3)
        self.flex_grid_sizer.AddGrowableCol(1, 6)
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
        
        self.choose_a_simpack_static_text.SetHelpText(
            self.simpack_tree.GetHelpText()
        )
        #                                                                     #
        ### Finished building simpack tree. ###################################
        
        ### Building simpack info panel: ######################################
        #                                                                     #
        self.simpack_info_panel = SimpackInfoPanel(self)
        self.flex_grid_sizer.Add(self.simpack_info_panel,
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
        self.create_project_button.SetHelpText('Start a new simulation '
                                               'project using the selected '
                                               'simpack.')
        
        self.cancel_button = wx.Button(self, wx.ID_CANCEL, 'Cancel')
        
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
        #                                                                     #
        ### Finished creating Ok/Cancel buttons. ##############################
        
        ### Creating context-help button (on GTK/Mac only): ###################
        #                                                                     #
        self.context_help_button_panel = CutePanel(self)
        self.context_help_button_panel.set_good_background_color()
        self.dialog_button_sizer.Add(
            self.context_help_button_panel,
            proportion=2,
            flag=wx.EXPAND
        )
        
        if wx_tools.is_win:
            self.context_help_button = None
        else:
            self.context_help_button = wx.ContextHelpButton(
                self.context_help_button_panel
            )
            self.context_help_button_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.context_help_button_panel.SetSizer(
                self.context_help_button_panel_sizer
            )
            self.context_help_button_panel_sizer.AddStretchSpacer(prop=1)
            self.context_help_button_panel_sizer.Add(
                self.context_help_button,
                proportion=0,
                flag=wx.ALIGN_BOTTOM
            )
        #                                                                     #
        ### Finished creating context-help button (on GTK/Mac only.) ##########
        
        
        self.Layout()
        self.simpack_tree.SetFocus()
        
        ### Setting reload triggers (button, hotkey and timer): ###############
        #                                                                     #
        self.reload_hidden_button = CuteHiddenButton(self)
        self.add_accelerators(
            {wx.WXK_F5: self.reload_hidden_button.Id}
        )
        self.reload_timer = CuteTimer(self)
        self.reload_timer.Start(10000)
        #                                                                     #
        ### Finished setting reload triggers (button, hotkey and timer). ######
        
        self.bind_event_handlers(SimpackSelectionDialog)

        
    @staticmethod
    def create_show_modal_and_return_simpack(frame):
        simpack_selection_dialog = SimpackSelectionDialog(frame)
        try:
            return_id = simpack_selection_dialog.ShowModal()
        finally:
            simpack_selection_dialog.Destroy()
        if return_id == wx.ID_OK:
            return simpack_selection_dialog.simpack
        
        
    def set_simpack_metadata(self, simpack_metadata):
        self.navigation_panel.set_simpack_metadata(simpack_metadata)
        
    
    def refresh(self):
        self.create_project_button.Enable(self.simpack_metadata is not None)
        self.simpack_tree.refresh()
        self.simpack_info_panel.refresh()
        self.navigation_panel.refresh()
        
        
    def EndModal(self, retCode):
        self.reload_timer.Stop()
        return CuteDialog.EndModal(self, retCode)
                

    def _on_reload_timer(self, event):
        self.simpack_tree.reload_tree()
        
        
    def _on_reload_hidden_button(self, event):
        self.simpack_tree.reload_tree()
                
        
    def _on_create_project_button(self, event):
        self.simpack = self.simpack_metadata.import_simpack() 
        self.EndModal(wx.ID_OK)
        
        
    def _on_cancel_button(self, event):
        self.EndModal(wx.ID_CANCEL)
        
                
    def _on_navigation_panel__back_button(self, event):
        self.navigation_panel.back()
        
        
    def _on_navigation_panel__forward_button(self, event):
        self.navigation_panel.forward()
        


from .navigation_panel import NavigationPanel
from .simpack_tree import SimpackTree
