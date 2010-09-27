import wx



class StatePlaceholder(wx.StaticText):
        def __init__(self, argument_list):
                wx.StaticText.__init__(self, argument_list, label='<state>')
                self.SetFont(argument_list.font)