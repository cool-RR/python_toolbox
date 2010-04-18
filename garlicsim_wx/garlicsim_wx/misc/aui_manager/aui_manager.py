#tododoc

import wx
from garlicsim_wx.general_misc.third_party import aui

class AuiManager(aui.AuiManager):
    def __init__(self, managed_window=None):
        aui.AuiManager.__init__(self, managed_window) # try aero flag
 
        self._art.SetMetric(aui.AUI_DOCKART_SASH_SIZE, 2)
        
        self._art.SetMetric(aui.AUI_DOCKART_CAPTION_SIZE, 10)
        self._art.SetFont(
            aui.AUI_DOCKART_CAPTION_FONT,
            wx.Font(7, wx.FONTFAMILY_MAX, wx.NORMAL, wx.NORMAL, False)
        )
        
        self._art.SetMetric(aui.AUI_DOCKART_GRADIENT_TYPE,
                            aui.AUI_GRADIENT_NONE)
        
        self._art.SetColor(aui.AUI_DOCKART_INACTIVE_CAPTION_COLOUR,
                           wx.Color(200, 200, 200))
