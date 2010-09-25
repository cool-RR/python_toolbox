import colorsys

import wx

from garlicsim_wx.widgets.general_misc.hue_control import HueControl

import garlicsim_wx


class HueControl(HueControl):
    # tododoc: possible confusion, this is called HueProfile in the
    # `step_profiles_controls` package, but it's good for a specific purpose,
    # and the dialog uses a different hue control.
    def __init__(self, step_profiles_list, step_profile, hue):
        HueControl.__init__(
            self,
            step_profiles_list.GetMainWindow(),
            lightness=0.8,
            saturation=1,
            size=(25, 10)
        )
                
        self.step_profiles_list = step_profiles_list
        self.frame = self.step_profiles_list.frame
        self.step_profile = step_profile
        self.hue = hue
      
        
    def open_editing_dialog(self):
        old_hls = wx_tools.wx_color_to_hls(self.color)
        gui_project = self.step_profiles_list.frame.gui_project
        step_profiles_to_hues = gui_project.step_profiles_to_hues
        
        getter = lambda: \
                 step_profiles_to_hues.__getitem__(self.step_profile)
        setter = lambda color: \
                 step_profiles_to_hues.__setitem__(self.step_profile, color)
        
        hue_selection_dialog = \
            HueSelectionDialog(self.frame, getter, setter, lightness=0.8,
                               title='Select hue for step profile')
        
        gui_project.step_profiles_to_hues_modified_emitter.add_output(
            hue_selection_dialog.update
        )
        try:
            hue_selection_dialog.ShowModal()
        finally:
            hue_selection_dialog.Destroy()
            gui_project.step_profiles_to_hues_modified_emitter.remove_output(
                hue_selection_dialog.update
            )

            
