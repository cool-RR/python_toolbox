#tododoc

import wx
from garlicsim_wx.general_misc.third_party import aui

class AuiDockArt(aui.AuiDefaultDockArt):
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
