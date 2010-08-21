# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

import pkg_resources
import wx

import garlicsim, garlicsim_wx

from .step_profiles_list import StepProfilesList

from . import images as __images_package
images_package = __images_package.__name__

    
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
        
        new_image = wx.BitmapFromImage(
            wx.ImageFromStream(
                pkg_resources.resource_stream(images_package,
                                              'new.png'),
                wx.BITMAP_TYPE_ANY
            )
        )
        self.new_button = wx.BitmapButton(self, -1, new_image)
        self.new_button.SetToolTipString('Create a new step profile.')
        
        self.button_h_sizer.Add(self.new_button, 0, wx.RIGHT, 8)
        
        delete_image = wx.BitmapFromImage(
            wx.ImageFromStream(
                pkg_resources.resource_stream(images_package,
                                              'trash.png'),
                wx.BITMAP_TYPE_ANY
            )
        )
        self.delete_button = wx.BitmapButton(self, -1, delete_image)
        self.delete_button.SetToolTipString(
            'Delete the selected step profile.'
        )
        
        self.button_h_sizer.Add(self.delete_button, 0, wx.RIGHT, 8)
        
        self.SetSizer(self.main_v_sizer)
        

