
from garlicsim_wx.widgets.general_misc.cute_dialog import CuteDialog

class AlreadyExistsDialog(CuteDialog):
    def __init__(self, step_profile_dialog, step_profile):
        self.step_profile_dialog = step_profile_dialog
        CuteDialog.__init__(self, step_profile_dialog,
                            title='Step profile already exists')

        self.main_v_sizer
        
        self.static_text
        'The step profile `%s` already exists.'
        'Take me to it'
        'Keep editing'
        