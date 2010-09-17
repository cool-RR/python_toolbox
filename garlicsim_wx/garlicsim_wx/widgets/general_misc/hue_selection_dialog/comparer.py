import wx


class Comparer(wx.Panel):
    def __init__(self, hue_selection_dialog):
        wx.Panel.__init__(self, parent=hue_selection_dialog, size=(75, 150),
                          style=wx.SUNKEN_BORDER)
        self.hue_selection_dialog = hue_selection_dialog