import wx

class Shell(wx.ScrolledWindow):
    """
    A Python shell widget.
    """
    def __init__(self,parent,id,gui_project=None,*args,**kwargs):
        wx.ScrolledWindow.__init__(self, parent, id, size=(400,-1))
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.gui_project=gui_project
        self.sizer=wx.BoxSizer(wx.HORIZONTAL)

        self.text_ctrl=wx.TextCtrl(self,-1, size=self.GetSize(), style=wx.TE_MULTILINE)
        self.text_ctrl.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Courier New'))

        self.sizer.Add(self.text_ctrl,1,wx.EXPAND)

        self.SetSizer(self.sizer)
        #self.sizer.Fit(self)





    def OnSize(self,e):
        self.Refresh()
