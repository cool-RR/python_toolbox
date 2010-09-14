import wx

import garlicsim_wx

from .color_control import ColorControl


class StepProfileEntry(wx.Window):
    def __init__(self, step_profiles_list, step_profile):
        
        self.step_profiles_list = step_profiles_list
        self.gui_project = step_profiles_list.gui_project
        assert isinstance(self.gui_project, garlicsim_wx.GuiProject)
        self.step_profile = step_profile
        
        wx.Window.__init__(self, step_profiles_list.GetMainWindow())
        
        self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.h_sizer)
        
        self.color_control = ColorControl(
            self,
            self.gui_project.step_profiles_to_hues[step_profile]
        )
        self.h_sizer.Add(self.color_control, 0, wx.RIGHT, border=10)
        
        
        