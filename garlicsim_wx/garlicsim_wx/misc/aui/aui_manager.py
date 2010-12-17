# Copyright 2009-2011 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
This module defines the `AuiManager` class.

See its documentation for more info.
'''

import wx
from garlicsim_wx.general_misc.third_party import aui

from .aui_dock_art import AuiDockArt
from .aui_tab_art import AuiTabArt


class AuiManager(aui.AuiManager):
    '''An AUI manager. See documentation of base class.'''
    def __init__(self, managed_window=None):
        aui.AuiManager.__init__(self, managed_window)
 
        self.SetArtProvider(AuiDockArt())
        
        self.tab_art_provider = AuiTabArt()
        
        self.SetAutoNotebookTabArt(self.tab_art_provider)
        
        
        
    def CreateNotebook(self):
        
        notebook = aui.AuiManager.CreateNotebook(self)

        notebook.SetNormalFont(self.tab_art_provider.GetNormalFont())
        notebook.SetSelectedFont(self.tab_art_provider.GetSelectedFont())
        notebook.SetMeasuringFont(self.tab_art_provider.GetMeasuringFont())
                
        
        return notebook
