import wx

from .color_control import ColorControl

class StepProfileEntry(wx.Window):
    def __init__(self, step_profiles_list, step_profile):
        self.step_profiles_list = step_profiles_list
        self.gui_project = step_profiles_list.gui_project
        self.step_profile = step_profile
        
        wx.Window.__init__(self, step_profiles_list.GetMainWindow())
        
        self.color_control = ColorControl(self