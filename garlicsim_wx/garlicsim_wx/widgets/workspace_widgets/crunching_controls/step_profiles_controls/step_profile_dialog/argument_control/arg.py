import wx

from garlicsim_wx.general_misc import wx_tools

from .value_text_ctrl import ValueTextCtrl


class Arg(wx.Panel):
    def __init__(self, argument_control, name, value=''):
        wx.Panel.__init__(self, argument_control)
        if wx.Platform == '__WXGTK__':
            self.SetBackgroundColour(wx_tools.get_background_color())
        
        self.argument_control = argument_control
        self.name = name
        
        self.main_h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.name_static_text = wx.StaticText(self, label=('%s: ' % name))
        
        self.main_h_sizer.Add(self.name_static_text, 0,
                              wx.ALIGN_CENTER_VERTICAL)
        
        self.value_text_ctrl = ValueTextCtrl(
            self,
            #size=(100, -1),
            value=value,
            root=argument_control.gui_project.simpack
        )
        
        self.main_h_sizer.Add(self.value_text_ctrl, 1,
                              wx.ALIGN_CENTER_VERTICAL)
        
        self.SetSizer(self.main_h_sizer)
        
        #self.main_h_sizer.Fit(self)
        
    def get_value_string(self):
        return self.value_text_ctrl.GetValue()