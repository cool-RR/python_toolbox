# Copyright 2009-2011 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the `HueControl` class.

See its documentation for more details.
'''

import colorsys

import wx

from garlicsim_wx.widgets.general_misc.hue_control \
     import HueControl as GenericHueControl

import garlicsim_wx


class HueControl(GenericHueControl):
    '''
    Control for viewing and changing the hue associated with a step profile.
    '''
    def __init__(self, step_profile_item_panel, step_profile):
        
        self.step_profile = step_profile
        
        self.step_profile_item_panel = step_profile_item_panel
        self.frame = self.step_profile_item_panel.frame
        self.gui_project = self.frame.gui_project
        
        getter = lambda: \
               self.gui_project.step_profiles_to_hues.__getitem__(
                   self.step_profile
               )
        
        setter = lambda hue: \
               self.gui_project.step_profiles_to_hues.__setitem__(
                   self.step_profile,
                   hue
               )
        
        size = (25, 15)
        
        GenericHueControl.__init__(
            self,
            step_profile_item_panel,
            getter=getter,
            setter=setter,
            emitter=self.gui_project.step_profiles_to_hues_modified_emitter,
            lightness=0.8,
            saturation=1,
            dialog_title='Select hue for step profile',
            size=size
        )
        
        self.SetMinSize(size)

        self.SetBackgroundColour(step_profile_item_panel.GetBackgroundColour())
        
        
            
