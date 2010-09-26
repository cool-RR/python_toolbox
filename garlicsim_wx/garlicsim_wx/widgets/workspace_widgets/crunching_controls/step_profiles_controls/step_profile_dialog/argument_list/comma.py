import wx



class Comma(wx.StaticText):
    def __init__(self, argument_list):
        wx.StaticText.__init__(self, argument_list, label=', ')
        self.SetFont(argument_list.font)