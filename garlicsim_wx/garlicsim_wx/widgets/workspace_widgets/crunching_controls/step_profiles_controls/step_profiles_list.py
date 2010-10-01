# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

import pkg_resources
import wx
import weakref

from garlicsim_wx.general_misc.third_party import aui
from garlicsim_wx.general_misc.flag_raiser import FlagRaiser
from garlicsim_wx.general_misc import emitters
from garlicsim_wx.general_misc import wx_tools
from garlicsim_wx.widgets.general_misc import cute_hyper_tree_list

import garlicsim, garlicsim_wx
from garlicsim_wx.widgets import WorkspaceWidget
from garlicsim_wx.misc.colors import hue_to_light_color


from .hue_control import HueControl
from .blank_context_menu import BlankContextMenu
from .step_profile_context_menu import StepProfileContextMenu


class StepProfilesList(cute_hyper_tree_list.CuteHyperTreeList):
    '''tododoc'''
    # tododoc: set max size dynamically according to number of profiles
    
    def __init__(self, step_profiles_controls, frame):
        
        self.frame = frame
        assert isinstance(self.frame, garlicsim_wx.Frame)
        self.gui_project = frame.gui_project
        assert isinstance(self.gui_project, garlicsim_wx.GuiProject)
        self.step_profiles_controls = step_profiles_controls
        
        cute_hyper_tree_list.CuteHyperTreeList.__init__(
            self,
            step_profiles_controls,
            style=wx.SIMPLE_BORDER,
            agwStyle=(
                wx.TR_FULL_ROW_HIGHLIGHT | \
                wx.TR_ROW_LINES | \
                wx.TR_HIDE_ROOT | \
                cute_hyper_tree_list.TR_NO_HEADER
                )
        )        
        
        self.step_profiles_to_items = weakref.WeakKeyDictionary()
        
        self.AddColumn('', width=50)
        self.AddColumn('', width=300)
        self.SetMainColumn(0)
        self.root_item = self.AddRoot('')
        
        self.items = self.root_item._children
        
        self.blank_context_menu = BlankContextMenu(self)
        self.step_profile_context_menu = StepProfileContextMenu(self)
        
        
        self.Bind(wx.EVT_TREE_ITEM_MENU, self.on_tree_item_menu)
        self.Bind(wx.EVT_CONTEXT_MENU, self.on_context_menu)
        
        
        self.Bind(wx.EVT_TREE_BEGIN_DRAG, self.on_tree_begin_drag)
        
        
        self.gui_project.step_profiles_set_modified_emitter.add_output(
            self.update
        )
        
  
        
    def update(self):
        
        gui_project = self.gui_project

        for step_profile in gui_project.step_profiles:
            try:
                item = self.step_profiles_to_items[step_profile]
            except KeyError:
                hue_control = HueControl(self, step_profile)
                item = self.AppendItem(self.root_item, '', ct_type=0, #2,
                                       wnd=hue_control)
                item.step_profile = step_profile
                item.hue_control = hue_control
                self.step_profiles_to_items[step_profile] = item
                self.SetItemText(
                    item,
                    step_profile.__repr__(short_form=True,
                                          root=gui_project.simpack,
                                          namespace=gui_project.namespace),
                    1
                )
                
            item.hue_control.SetSize((item.hue_control.GetSize()[0],
                                       item.GetHeight() - 4))
        
        for item in self.items:
            if item.step_profile not in gui_project.step_profiles:
                self.Delete(item)
                item.hue_control.Destroy()
                
                
    
    def get_selected_step_profile(self):
        
        selection = self.GetSelection()
        # Checking it's not the root:
        if selection and (not selection.HasChildren()):
            return selection.step_profile
        else:
            return None


    def delete_step_profile(self, step_profile):
        1/0 # tododoc
    
    
    def on_tree_item_menu(self, event):
        abs_position = event.GetPoint()
        
        if abs_position == wx.DefaultPosition:
            position = (0, 0) # todo: take position smartly
        else:
            position = self.ScreenToClient(abs_position)
            
        self.PopupMenu(self.step_profile_context_menu, position)
    
            
    def on_context_menu(self, event):

        abs_position = event.GetPosition()
        
        if abs_position == wx.DefaultPosition:
            position = (0, 0)
        else:
            position = self.ScreenToClient(abs_position)
            
        self.PopupMenu(self.blank_context_menu, position)
        
        
    def on_new_step_profile_button(self, event):
        self.step_profiles_controls.show_step_profile_editing_dialog()

        
    def on_fork_by_crunching_button(self, event):
        self.gui_project.fork_by_crunching(
            self.get_selected_step_profile()
        )

        
    def on_select_tree_members_button(self, event):
        raise NotImplementedError()

        
    def on_change_color_button(self, event):
        item = self.GetSelection()
        item.hue_control.open_editing_dialog()

        
    def on_duplicate_and_edit_button(self, event):
        self.step_profiles_controls.show_step_profile_editing_dialog(
            self.get_selected_step_profile()
        )

        
    def on_delete_button(self, event):
        self.delete_step_profile(self.get_selected_step_profile())
    
        
    def on_tree_begin_drag(self, event):
        event.Allow()
        
        
    def on_tree_end_drag(self, event):
        event.Allow()