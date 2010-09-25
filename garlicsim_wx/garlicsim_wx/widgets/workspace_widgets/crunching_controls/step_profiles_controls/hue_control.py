import colorsys

import wx

from garlicsim_wx.widgets.general_misc.hue_control \
     import HueControl as GenericHueControl

import garlicsim_wx


class HueControl(GenericHueControl):
    # tododoc: possible confusion, this is called HueProfile in the
    # `step_profiles_controls` package, but it's good for a specific purpose,
    # and the dialog uses a different hue control.
    def __init__(self, step_profiles_list, step_profile, hue):
        
        self.step_profile = step_profile
        
        self.step_profiles_list = step_profiles_list
        self.frame = self.step_profiles_list.frame
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
        
        GenericHueControl.__init__(
            self,
            step_profiles_list.GetMainWindow(),
            getter=getter,
            setter=setter,
            emitter=self.gui_project.step_profiles_to_hues_modified_emitter,
            lightness=0.8,
            saturation=1,
            dialog_title='Select hue for step profile',
            size=(25, 10)
        )
                
        
            
