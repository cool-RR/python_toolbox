import life
import wx
from guiproject import *

class LifeGuiProject(GuiProject):
    def __init__(self,*args,**kwargs):
        GuiProject.__init__(self,*args,**kwargs)
        self.mysizer=wx.BoxSizer(wx.VERTICAL)
        self.mytextctrl=wx.TextCtrl(self.state_showing_window, -1, style=wx.TE_MULTILINE)
        self.mytextctrl.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Courier New'))
        self.mysizer.Add(self.mytextctrl,1,wx.EXPAND)
        self.state_showing_window.SetSizer(self.mysizer)
        self.mysizer.Fit(self.state_showing_window)

    def show_state(self,state):
        self.mytextctrl.SetValue(str(state.board))

