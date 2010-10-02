
import wx

class StepProfileIndicator(wx.Panel):
    def __init__(self, step_profiles_list,):
        self.step_profiles_list = step_profiles_list
        wx.Panel.__init__(
            self,
            step_profiles_list.GetMainWindow()
            )