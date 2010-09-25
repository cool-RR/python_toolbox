import wx

from garlicsim_wx.general_misc import wx_tools

import garlicsim


class StaticFunctionText(wx.StaticText):
    # center align, have some redness when not a (step) function
    def __init__(self, step_profile_dialog):
        
        self.step_profile_dialog = step_profile_dialog
        
        wx.StaticText.__init__(self, step_profile_dialog,
                               style=wx.ALIGN_CENTER)
        self.SetBackgroundColour(wx_tools.get_background_color())
        self.Wrap(self.GetClientSize()[0] - 20)
        
        self.Bind(wx.EVT_SIZE, self.on_size)
        
        self._error_color = wx.Color(255, 200, 200)
        
        
    def set_error_text(self, error_text):
        self.SetLabel(error_text)
        self.SetBackgroundColour(self._error_color)
        
        
    def set_step_function(self, step_function):
        label = '%s is a %s.' % (
            self.step_profile_dialog.step_function_to_address(step_function),
            garlicsim.misc.simpack_grokker.get_step_type(step_function)
        )
        self.SetLabel(label)
        self.SetBackgroundColour(wx_tools.get_background_color())

    
    def on_size(self, event):
        self.Wrap(self.GetClientSize()[0] - 20)