#tododoc

import wx
from garlicsim_wx.general_misc.third_party import aui

from aui_dock_art import AuiDockArt
from aui_tab_art import AuiTabArt

class AuiManager(aui.AuiManager):
    def __init__(self, managed_window=None):
        aui.AuiManager.__init__(self, managed_window) # todo: try aero and whidbey flags
 
        self.SetArtProvider(AuiDockArt())
        
        self.TabArtProvider = AuiTabArt
        
    def CreateNotebook(self):
        notebook = aui.AuiManager.CreateNotebook(self)
        notebook.SetArtProvider(self.TabArtProvider())
        return notebook
