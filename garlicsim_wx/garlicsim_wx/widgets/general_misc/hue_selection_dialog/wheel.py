import wx


class Wheel(wx.Panel):
    def __init__(self, hue_selection_dialog):
        wx.Panel.__init__(self, parent=hue_selection_dialog, size=(300, 300))
        self.hue_selection_dialog = hue_selection_dialog
        self.lightness = hue_selection_dialog.lightness
        self.saturation = hue_selection_dialog.saturation