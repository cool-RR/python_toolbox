import wx


class StaticFunctionText(wx.StaticText):
    # center align, have some redness when not a (step) function
    def __init__(self, step_profile_dialog):
        
        self.step_profile_dialog = step_profile_dialog
        
        wx.StaticText.__init__(self, step_profile_dialog)
        
        