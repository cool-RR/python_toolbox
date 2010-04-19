#tododoc

import wx
from garlicsim_wx.general_misc.third_party import aui

from aui_dock_art import AuiDockArt
from aui_tab_art import AuiTabArt

class AuiManager(aui.AuiManager):
    def __init__(self, managed_window=None):
        aui.AuiManager.__init__(self, managed_window)
 
        self.SetArtProvider(AuiDockArt())
        
        self.TabArtProvider = AuiTabArt
        
        
    def CreateNotebook(self):

        notebook = aui.AuiManager.CreateNotebook(self)

        tab_art_provider = self.TabArtProvider()

        notebook.SetArtProvider(tab_art_provider)
        
        notebook.SetNormalFont(tab_art_provider.GetNormalFont())
        notebook.SetSelectedFont(tab_art_provider.GetSelectedFont())
        notebook.SetMeasuringFont(tab_art_provider.GetMeasuringFont())
        
        return notebook
