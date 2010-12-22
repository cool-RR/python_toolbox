# Copyright 2009-2011 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the `StepProfileItemPanel` class.

See its documentation for more details.
'''

import wx

from .active_step_profile_indicator import ActiveStepProfileIndicator
from .hue_control import HueControl


class StepProfileItemPanel(wx.Panel):
    '''
    Panel to display next to a step profile in the step profiles list.
    
    This panel contains:
    
     1. `ActiveStepProfileIndicator` for indicating which step profile is 
        active.
        
     2. `HueControl` for viewing and changing the hue associated with a step
        profile.
        
    '''
    def __init__(self, step_profiles_list, step_profile):
        self.step_profiles_list = step_profiles_list
        self.frame = step_profiles_list.frame
        self.step_profile = step_profile
        wx.Panel.__init__(
            self,
            step_profiles_list.GetMainWindow(),
            size=(40, 20)
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
                              wx.EXPAND | wx.TOP | wx.BOTTOM, border=3)
        
        self.main_h_sizer.AddSpacer((5, -1))
        
        self.hue_control = HueControl(self, step_profile)
        
        self.main_h_sizer.Add(self.hue_control, 0,
                              wx.EXPAND | wx.BOTTOM | wx.TOP, border=3)
        
        self.SetSizer(self.main_h_sizer)
        self.Layout()
        
        