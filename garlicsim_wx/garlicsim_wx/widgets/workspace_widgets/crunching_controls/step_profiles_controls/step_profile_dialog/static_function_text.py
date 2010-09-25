import wx

from garlicsim_wx.general_misc import wx_tools

import garlicsim


class StaticFunctionText(wx.StaticText):
    # center align, have some redness when not a (step) function
    def __init__(self, step_profile_dialog):
        
        self.step_profile_dialog = step_profile_dialog
        
        wx.StaticText.__init__(self, step_profile_dialog,
                               style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.SetMinSize((300, 25))
        self.SetBackgroundColour(wx_tools.get_background_color())
        self.Wrap(300)
        
        self.Bind(wx.EVT_SIZE, self.on_size)
        
        self._error_color = wx.Color(255, 200, 200)
        self._success_color = wx.Color(200, 255, 200)
        
        
    def set_error_text(self, error_text):
        self.SetLabel(error_text)
        self.Wrap(300)
        self.SetBackgroundColour(self._error_color)
        #self.step_profile_dialog.main_v_sizer.Fit(self.step_profile_dialog)
        #self.Fit()
        
        
    def set_step_function(self, step_function):
        step_type = garlicsim.misc.simpack_grokker.get_step_type(step_function)
        label = '%s is a %s.' % (
            self.step_profile_dialog.step_function_to_address(step_function),
            step_type.verbose_name
        )
        self.SetLabel(label)
        self.Wrap(300)
        self.SetBackgroundColour(self._success_color)

    
    def on_size(self, event):
        0#self.Wrap(self.GetSize()[0])