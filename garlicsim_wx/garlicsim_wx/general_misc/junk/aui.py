import wx
import wx.lib.agw.aui as aui
from wx.lib.agw.aui import *

class MyFrame(wx.Frame):

    def __init__(self, parent, id=-1, title="AUI Test", pos=wx.DefaultPosition,
                 size=(800, 600), style=wx.DEFAULT_FRAME_STYLE):

        wx.Frame.__init__(self, parent, id, title, pos, size, style)

        self._mgr = aui.AuiManager()
        
        # notify AUI which frame to use
        self._mgr.SetManagedWindow(self)

        # create several text controls
        text1 = wx.TextCtrl(self, -1, "Pane 1 - sample text",
                            wx.DefaultPosition, wx.Size(200,150),
                            wx.NO_BORDER | wx.TE_MULTILINE)
                                           
        text2 = wx.TextCtrl(self, -1, "Pane 2 - sample text",
                            wx.DefaultPosition, wx.Size(200,150),
                            wx.NO_BORDER | wx.TE_MULTILINE)
                                           
        text3 = wx.TextCtrl(self, -1, "Main content window",
                            wx.DefaultPosition, wx.Size(200,150),
                            wx.NO_BORDER | wx.TE_MULTILINE)
        
        # add the panes to the manager
        self._mgr.AddPane(text1, AuiPaneInfo().Left().Caption("Pane Number One"))
        self._mgr.AddPane(text2, AuiPaneInfo().Bottom().Caption("Pane Number Two"))
        self._mgr.AddPane(text3, AuiPaneInfo().CenterPane())
                              
        # tell the manager to "commit" all the changes just made
        self._mgr.Update()

        self.Bind(wx.EVT_CLOSE, self.OnClose)


    def OnClose(self, event):

        # deinitialize the frame manager
        self._mgr.UnInit()

        self.Destroy()        
        event.Skip()        


# our normal wxApp-derived class, as usual

app = wx.PySimpleApp()

frame = MyFrame(None)
app.SetTopWindow(frame)
frame.Show()

app.MainLoop()