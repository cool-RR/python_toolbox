# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

import pkg_resources
import wx
import weakref
from garlicsim_wx.general_misc.third_party import hypertreelist
from garlicsim_wx.general_misc.third_party import customtreectrl

from garlicsim_wx.general_misc.third_party import aui
from garlicsim_wx.general_misc.flag_raiser import FlagRaiser
from garlicsim_wx.general_misc import emitters
from garlicsim_wx.general_misc import wx_tools

import garlicsim, garlicsim_wx
from garlicsim_wx.widgets import WorkspaceWidget
from garlicsim_wx.misc.colors import hue_to_light_color

from .color_control import ColorControl


EVT_COMMAND_TREE_ITEM_RIGHT_CLICK = \
    wx.PyEventBinder(wx.wxEVT_COMMAND_TREE_ITEM_RIGHT_CLICK, 1)


class StepProfilesList(hypertreelist.HyperTreeList):
    '''tododoc'''
    # tododoc: set max size dynamically according to number of profiles
    
    def __init__(self, parent, frame):
        
        self.frame = frame
        assert isinstance(self.frame, garlicsim_wx.Frame)
        self.gui_project = frame.gui_project
        assert isinstance(self.gui_project, garlicsim_wx.GuiProject)
        
        hypertreelist.HyperTreeList.__init__(
            self,
            parent,
            style=wx.SIMPLE_BORDER,
            agwStyle=(
                wx.TR_FULL_ROW_HIGHLIGHT | \
                wx.TR_ROW_LINES | \
                wx.TR_HIDE_ROOT | \
                hypertreelist.TR_NO_HEADER
                )
        )        
        
        self.step_profiles_to_items = weakref.WeakKeyDictionary()
        
        self.AddColumn('', width=50)
        self.AddColumn('', width=150)
        self.SetMainColumn(0)
        self.root_item = self.AddRoot('')
        
        self.items = self.root_item._children
        
        
        # Hackishly generating context menu event and tree item menu event from
        # these three events:
        self.Bind(EVT_COMMAND_TREE_ITEM_RIGHT_CLICK,
                  self.on_command_tree_item_right_click)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        self.Bind(wx.EVT_RIGHT_UP, self.on_right_up)
        
        self.Bind(wx.EVT_TREE_ITEM_MENU, self.on_tree_item_menu)
        self.Bind(wx.EVT_CONTEXT_MENU, self.on_context_menu)
        
        
        
        self.gui_project.step_profiles_set_modified_emitter.add_output(
            self.update
        )
        
        self.gui_project.step_profiles_to_hues_modified_emitter.add_output(
            self.update_colors
        )
        
  
        
    def update(self):

        for step_profile in self.gui_project.step_profiles:
            try:
                item = self.step_profiles_to_items[step_profile]
            except KeyError:
                color = hue_to_light_color(
                    self.gui_project.step_profiles_to_hues[step_profile]
                )
                color_control = ColorControl(self, step_profile, color)
                item = self.AppendItem(self.root_item, '', ct_type=2, wnd=color_control)
                item.step_profile = step_profile
                item.color_control = color_control
                self.step_profiles_to_items[step_profile] = item
                self.SetItemText(
                    item,
                    step_profile.__repr__(short_form=True,
                                          root=self.gui_project.simpack),
                    1
                )
                
            item.color_control.SetSize((item.color_control.GetSize()[0],
                                       item.GetHeight() - 4))
        
        for item in self.items:
            if item.step_profile not in self.gui_project.step_profiles:
                self.Delete(item)
                item.color_control.Destroy()
                
                
    def update_colors(self):
        
        for item in self.items:
            color = hue_to_light_color(
                self.gui_project.step_profiles_to_hues[
                    item.step_profile
                ]
            )
            item.color_control.set_color(color)
            

    # tododoc: move these (and bindings) to my HyperTreeList subclass:
    
    def on_command_tree_item_right_click(self, event):
        
        event = hypertreelist.TreeEvent(
            customtreectrl.wxEVT_TREE_ITEM_MENU,
            self.GetId(),
            item=event.GetItem()
        )
        event.SetEventObject(self)
        wx.PostEvent(self, event)
        
        
    def on_right_up(self, event):
        item = self._main_win._anchor.HitTest(
            self._main_win.CalcUnscrolledPosition(
                wx.Point(event.GetX(), event.GetY())
                ),
            self._main_win,
            0,
            self._main_win._curColumn,
            0
        )[0]
        if item:
            assert item is self.GetSelection()
            
            event = hypertreelist.TreeEvent(
                customtreectrl.wxEVT_TREE_ITEM_MENU,
                self.GetId(),
                item=item
            )
            event.SetEventObject(self)
            wx.PostEvent(self, event)
            #self.GetEventHandler().ProcessEvent(event)
            
        else:
            wx_tools.post_event(self, wx.EVT_CONTEXT_MENU, self)
        
            
    def on_key_down(self, event):
        # Hacky, either the OS or wxPython should be doing this:
        key = wx_tools.Key.get_from_key_event(event)
        if key in wx_tools.menu_keys:
            selection = self.GetSelection()
            if selection is not None:
                
                event = hypertreelist.TreeEvent(
                    customtreectrl.wxEVT_TREE_ITEM_MENU,
                    self.GetId(),
                    item=selection
                )
                event.SetEventObject(self)
                self.GetEventHandler().ProcessEvent(event)
                
            else:
                wx_tools.post_event(self, wx.EVT_CONTEXT_MENU, self)
        else:
            event.Skip()
        
        
            
    def on_tree_item_menu(self, event):
        raise str(event._item)
        pass
    
            
    def on_context_menu(self, event):
        1/0
        pass
    