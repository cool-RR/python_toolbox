import wx

from garlicsim_wx.general_misc import wx_tools

import garlicsim


class StaticFunctionText(wx.Panel):
    def __init__(self, step_profile_dialog):
        
        self.step_profile_dialog = step_profile_dialog
        
        self.step_function = None
        
        wx.Panel.__init__(self, step_profile_dialog)
        
        self.SetBackgroundColour(wx_tools.get_background_color())
        
        self.text = wx.StaticText(self, style=wx.ALIGN_CENTER_HORIZONTAL)
        
        self.SetMinSize((300, 25))
        
        self.text.SetBackgroundColour(wx_tools.get_background_color())
        
        self.text.Wrap(300)
        
        self.Bind(wx.EVT_SIZE, self.on_size)
        
        self.main_h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.main_h_sizer.Add(self.v_sizer, 1, wx.ALIGN_CENTER_VERTICAL)
        
        self.v_sizer.Add(self.text, 0, wx.ALIGN_CENTER_HORIZONTAL)
        
        self.SetSizer(self.main_h_sizer)
        
        self._error_color = wx.Color(255, 200, 200)
        self._success_color = wx.Color(200, 255, 200)
        
        
    def set_error_text(self, error_text):
        self.text.SetLabel(error_text)
        self.text.Wrap(300)
        self.text.SetBackgroundColour(self._error_color)
        #self.step_profile_dialog.main_v_sizer.Fit(self.step_profile_dialog)
        #self.Fit()
        
        
    def set_step_function(self, step_function):
        if step_function != self.step_function:
            step_type = garlicsim.misc.simpack_grokker.get_step_type(step_function)
            label = '%s is a %s.' % (
                self.step_profile_dialog.step_function_to_address(step_function),
                step_type.verbose_name
            )
            self.text.SetLabel(label)
            self.text.Wrap(300)
            self.text.SetBackgroundColour(self._success_color)

    
    def on_size(self, event):
        0#self.Wrap(self.GetSize()[0])