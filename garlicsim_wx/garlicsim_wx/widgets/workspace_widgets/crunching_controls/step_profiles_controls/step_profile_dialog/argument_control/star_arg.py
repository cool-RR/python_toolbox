import wx

from garlicsim_wx.general_misc import wx_tools



class StarArg(wx.Panel):
    def __init__(self, argument_control, star_arg_box, value='', last=False):
        wx.Panel.__init__(self, argument_control)
        if wx.Platform == '__WXGTK__':
            self.SetBackgroundColour(wx_tools.get_background_color())
        
        self.argument_control = argument_control
        
        self.star_arg_box = star_arg_box
        
        self.last = last
        
        self.main_h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.text_ctrl = wx.TextCtrl(self, value=value)
        
        self.main_h_sizer.Add(self.text_ctrl, 1,
                              wx.ALIGN_CENTER_VERTICAL)
        
        self.SetSizer(self.main_h_sizer)
        
        self.Bind(wx.EVT_TEXT, self.on_text)
        
        self.Bind(wx.EVT_KILL_FOCUS, self.on_kill_focus)

        
    def on_text(self, event):
        if self.last:
            if self.text_ctrl.GetValue():
                self.star_arg_box.organize()
            
            
    def	on_kill_focus(self, event):
        event.Skip()
        if self.FindFocus() != self:
            self.star_arg_box.organize()
            