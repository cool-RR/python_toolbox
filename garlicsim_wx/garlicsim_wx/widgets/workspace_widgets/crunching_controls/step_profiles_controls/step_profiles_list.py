# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

import pkg_resources
import wx
import weakref
from garlicsim_wx.general_misc.third_party import hypertreelist

from garlicsim_wx.general_misc.third_party import aui
from garlicsim_wx.general_misc.flag_raiser import FlagRaiser
from garlicsim_wx.general_misc import emitters

import garlicsim, garlicsim_wx
from garlicsim_wx.widgets import WorkspaceWidget
from garlicsim_wx.misc.colors import hue_to_dark_color

from .step_profile_entry import StepProfileEntry
from .x_color_control import XColorControl


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
        
        #self.static_text = wx.StaticText(self.GetMainWindow(), -1, 'boobiesqqq')
        
        #item = self.AppendItem(self.root_item, '', ct_type=1, wnd=self.static_text)
        #self.SetItemText(item, 'muaww', 1)
        
        
        #self.AppendItem(self.root_item, 'ass', ct_type=2, wnd=None)
        #self.AppendItem(self.root_item, 'tits', ct_type=2, wnd=None)
        
        self.gui_project.step_profiles_set_modified_emitter.add_output(
            self.update
        )
  
        
    def update(self):

        for step_profile in self.gui_project.step_profiles:
            color = hue_to_dark_color(
                self.gui_project.step_profiles_to_hues[step_profile]
            )
            try:
                item = self.step_profiles_to_items[step_profile]
            except KeyError:
                #entry = StepProfileEntry(self, step_profile)
                color_control = XColorControl(self, color)
                item = self.AppendItem(self.root_item, '', ct_type=2, wnd=color_control)
                item.step_profile = step_profile
                item.color_control = color_control
                self.step_profiles_to_items[step_profile] = item
            else:
                item.color_control.set_color(color)
        
            self.SetItemText(item, step_profile.__repr__(short_form=True), 1)
            item.color_control.SetSize((item.color_control.GetSize()[0],
                                       item.GetHeight() - 4))
        
        for item in self.items:
            if item.step_profile not in self.gui_project.step_profiles:
                self.Delete(item)