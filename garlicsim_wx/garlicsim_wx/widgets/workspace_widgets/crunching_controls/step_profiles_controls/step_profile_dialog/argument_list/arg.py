import wx



class Arg(wx.Panel):
    def __init__(self, argument_list, name, value=''):
        wx.Panel.__init__(self, argument_list)
        
        self.argument_list = argument_list
        self.name = name
        
        self.main_h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.name_static_text = wx.StaticText(self, label=('%s=' % name))
        
        self.name_static_text.SetFont(argument_list.font)
        
        self.main_h_sizer.Add(self.name_static_text, 0, wx.EXPAND)
        
        self.text_ctrl = wx.TextCtrl(self, size=(100, -1), value=value)
        
        self.main_h_sizer.Add(self.text_ctrl, 0, wx.EXPAND)
        
        self.SetSizer(self.main_h_sizer)