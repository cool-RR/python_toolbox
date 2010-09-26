import wx



class OpeningBracket(wx.StaticText):
    def __init__(self, argument_list):
        wx.StaticText.__init__(self, argument_list, label='(')
        self.SetFont(argument_list.bold_font)
        