
import wx

from .active_step_profile_indicator import ActiveStepProfileIndicator
from .hue_control import HueControl

class StepProfileItemPanel(wx.Panel):
    def __init__(self, step_profiles_list, step_profile):
        self.step_profiles_list = step_profiles_list
        self.frame = step_profiles_list.frame
        self.step_profile = step_profile
        wx.Panel.__init__(
            self,
            step_profiles_list.GetMainWindow()
        )
        
        
        self.SetBackgroundColour(
            step_profiles_list.GetMainWindow().GetBackgroundColour()
        )
        
        self.main_h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        
        self.active_step_profile_indicator = ActiveStepProfileIndicator(
            self,
            step_profile
        )
        
        self.main_h_sizer.Add(self.active_step_profile_indicator, 0,
                              wx.EXPAND | wx.RIGHT, border=5)
        
        
        self.hue_control = HueControl(self, step_profile)
        
        self.main_h_sizer.Add(self.hue_control, 0,
                              wx.EXPAND | wx.BOTTOM | wx.TOP, border=2)
        
        self.SetSizer(self.main_h_sizer)
        
        self.main_h_sizer.Fit(self)