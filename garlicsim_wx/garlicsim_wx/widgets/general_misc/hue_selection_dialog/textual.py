import wx


class Textual(wx.Panel):
    def __init__(self, hue_selection_dialog):
        wx.Panel.__init__(self, parent=hue_selection_dialog, size=(75, 100))
        self.hue_selection_dialog = hue_selection_dialog
        self.hue = hue_selection_dialog.hue
        
        self.main_v_sizer = wx.BoxSizer(wx.VERTICAL)
        
        
        
    def update(self):
        if self.hue != self.hue_selection_dialog.hue:
            self.hue = self.hue_selection_dialog.hue