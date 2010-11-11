
import wx

class CruncherTextScrolledPanel(wx.lib.scrolledpanel.ScrolledPanel):
    def __init__(self, cruncher_selection_dialog):
        wx.lib.scrolledpanel.ScrolledPanel.__init__(self, cruncher_selection_dialog)