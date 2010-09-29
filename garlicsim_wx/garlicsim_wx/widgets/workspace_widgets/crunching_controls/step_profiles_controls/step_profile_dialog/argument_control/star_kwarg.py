import wx

from garlicsim_wx.general_misc import wx_tools

from .close_button import CloseButton


class StarKwarg(wx.Panel):
    def __init__(self, argument_control, star_kwarg_box, name='', value=''):
        wx.Panel.__init__(self, argument_control)
        if wx.Platform == '__WXGTK__':
            self.SetBackgroundColour(wx_tools.get_background_color())
        
        self.argument_control = argument_control
        
        self.star_kwarg_box = star_kwarg_box
        
        self.main_h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.name_text_ctrl = wx.TextCtrl(self, value=name)
        
        self.main_h_sizer.Add(self.name_text_ctrl, 0.4,
                              wx.ALIGN_CENTER_VERTICAL)
                
        self.static_text = wx.StaticText(self, label=(': ' % name))
        
        self.main_h_sizer.Add(self.star_kwarg_box, 0,
                              wx.ALIGN_CENTER_VERTICAL)
        
        self.value_text_ctrl = wx.TextCtrl(self, value=value)
        
        self.main_h_sizer.Add(self.value_text_ctrl, 0.6,
                              wx.ALIGN_CENTER_VERTICAL)
        
        self.close_button = CloseButton(self)
        
        self.main_h_sizer.Add(self.close_button, 0,
                              wx.ALIGN_CENTER_VERTICAL)
        
        self.SetSizer(self.main_h_sizer)
        
        self.Bind(wx.EVT_BUTTON, lambda event: self.remove(),
                  source=self.close_button)

        
    def remove(self):
        self.star_kwarg_box.remove(self)
        
        
    def get_name_string(self):
        return self.name_text_ctrl.GetValue()
    
    
    def get_value_string(self):
        return self.value_text_ctrl.GetValue()
        
        
        
            