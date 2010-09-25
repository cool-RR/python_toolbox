import wx



class StepFunctionInput(wx.ComboBox):
    def __init__(self, step_profile_dialog, value=''):
        self.step_profile_dialog = step_profile_dialog
        wx.ComboBox.__init__(self