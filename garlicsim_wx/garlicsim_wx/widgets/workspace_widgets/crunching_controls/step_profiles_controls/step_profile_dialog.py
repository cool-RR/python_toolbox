import wx

from garlicsim_wx.widgets.general_misc.cute_dialog import CuteDialog



def StepProfileDialog(CuteDialog):
    # tododoc: this class will be responsible for checking if the new step
    # profile is already present in the step_profiles set.
    
    def __init__(self, step_profiles_controls, step_profile=None):
        
        self.step_profiles_controls = step_profiles_controls
        assert isinstance(self.step_profiles_controls, StepProfileControls)
        
        CuteDialog.__init__(self, step_profiles_controls.frame,
                            title='Create a new step profile')
        
        self.original_step_profile = step_profile


from .step_profiles_controls import StepProfilesControls