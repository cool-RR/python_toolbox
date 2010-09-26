# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

import pkg_resources
import wx

from garlicsim_wx.general_misc import wx_tools

import garlicsim, garlicsim_wx

from .step_profiles_list import StepProfilesList
from .step_profile_dialog import StepProfileDialog

from . import images as __images_package
images_package = __images_package.__name__

    
class StepProfilesControls(wx.Panel):
    '''tododoc'''
    
    def __init__(self, parent, frame, *args, **kwargs):
        
        self.frame = frame
        assert isinstance(self.frame, garlicsim_wx.Frame)
        
        self.gui_project = frame.gui_project
        assert isinstance(self.gui_project, garlicsim_wx.GuiProject)
        
        wx.Panel.__init__(self, parent, *args, **kwargs)
        
        self.SetBackgroundColour(wx_tools.get_background_color())

        
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
        
            
    
    def open_step_profile_editing_dialog(self, step_profile=None):
        step_profile_dialog = StepProfileDialog(self, step_profile)
        
        try:
            if step_profile_dialog.ShowModal() == wx.ID_OK:
                new_step_profile = step_profile_dialog.step_profile
                new_hue = step_profile_dialog.hue
            else:
                new_step_profile = new_hue = None
        finally:
            step_profile_dialog.Destroy()
            
        if new_step_profile:
            assert new_step_profile not in self.gui_project.step_profiles
            self.gui_project.step_profiles_to_hues[new_step_profile] = new_hue
            self.gui_project.step_profiles.add(new_step_profile)
