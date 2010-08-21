# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

import pkg_resources
import wx

import garlicsim, garlicsim_wx

from .step_profiles_list import StepProfilesList

    
class StepProfilesControls(wx.Panel):
    '''tododoc'''
    
    def __init__(self, parent, frame, *args, **kwargs):
        
        assert isinstance(frame, garlicsim_wx.Frame)
        self.frame = frame
        
        wx.Panel.__init__(self, parent, *args, **kwargs)

        
        self.main_v_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.title_text = wx.StaticText(self, -1, 'Step profiles:')
        
        self.main_v_sizer.Add(self.title_text, 0, wx.ALL, 10)
        
        self.step_profiles_list = StepProfilesList(self, frame)
        
        self.main_v_sizer.Add(self.step_profiles_list, 1,
                              wx.EXPAND | wx.BOTTOM, 8)
        
        self.button_h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.main_v_sizer.Add(self.button_h_sizer, 0, wx.ALIGN_RIGHT)
        
        self.new_button = wx.BitmapButton(self, -1, wx.EmptyBitmap(20, 10))
        self.new_button.SetToolTipString('Create a new step profile.')
        
        self.button_h_sizer.Add(self.new_button, 0, wx.RIGHT, 8)
        
        self.delete_button = wx.BitmapButton(self, -1, wx.EmptyBitmap(20, 10))
        self.delete_button.SetToolTipString(
            'Delete the selected step profile.'
        )
        
        self.button_h_sizer.Add(self.delete_button, 0, wx.RIGHT, 8)
        
        self.SetSizer(self.main_v_sizer)
        

