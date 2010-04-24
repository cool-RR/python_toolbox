# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
This module defines the AuiDockArt class.

See its documentation for more info.
'''

import wx
from garlicsim_wx.general_misc.third_party import aui

class AuiDockArt(aui.AuiDefaultDockArt):
    '''A dock art provider.'''
    def __init__(self):
        aui.AuiDefaultDockArt.__init__(self)
 
        self.SetMetric(aui.AUI_DOCKART_SASH_SIZE, 2)
        
        self.SetMetric(aui.AUI_DOCKART_CAPTION_SIZE, 10)
        self.SetFont(
            aui.AUI_DOCKART_CAPTION_FONT,
            wx.Font(7, wx.FONTFAMILY_MAX, wx.NORMAL, wx.NORMAL, False)
        )
        
        self.SetMetric(aui.AUI_DOCKART_GRADIENT_TYPE,
                       aui.AUI_GRADIENT_NONE)
        
        self.SetColor(aui.AUI_DOCKART_INACTIVE_CAPTION_COLOUR,
                      wx.Color(200, 200, 200))
