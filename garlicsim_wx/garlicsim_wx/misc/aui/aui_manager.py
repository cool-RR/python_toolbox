# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
This module defines the AuiManager class.

See its documentation for more info.
'''

import wx
from garlicsim_wx.general_misc.third_party import aui

from aui_dock_art import AuiDockArt
from aui_tab_art import AuiTabArt


class AuiManager(aui.AuiManager):
    '''An AUI manager. See documentation of base class.'''
    def __init__(self, managed_window=None):
        aui.AuiManager.__init__(self, managed_window)
 
        self.SetArtProvider(AuiDockArt())
        
        self.TabArtProvider = AuiTabArt
        
        
    def CreateNotebook(self):
        
        # todo: try to use Andrea's new "automatic" notebook tab art provider
        
        notebook = aui.AuiManager.CreateNotebook(self)

        tab_art_provider = self.TabArtProvider()

        notebook.SetArtProvider(tab_art_provider)
        
        notebook.SetNormalFont(tab_art_provider.GetNormalFont())
        notebook.SetSelectedFont(tab_art_provider.GetSelectedFont())
        notebook.SetMeasuringFont(tab_art_provider.GetMeasuringFont())
        
        return notebook
