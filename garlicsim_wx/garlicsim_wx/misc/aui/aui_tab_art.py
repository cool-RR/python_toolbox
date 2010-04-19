#tododoc

import wx
from garlicsim_wx.general_misc.third_party import aui

class AuiTabArt(aui.AuiDefaultTabArt):
    def __init__(self):
        aui.AuiDefaultTabArt.__init__(self)
        
        self.SetNormalFont(wx.Font(7, wx.FONTFAMILY_MAX, wx.NORMAL, wx.NORMAL))
        self.SetSelectedFont(wx.Font(7, wx.FONTFAMILY_MAX, wx.NORMAL, wx.NORMAL))
        self.SetMeasuringFont(wx.Font(7, wx.FONTFAMILY_MAX, wx.NORMAL, wx.NORMAL))
 
    def Clone(self):

        art = type(self)()
        art.SetNormalFont(self.GetNormalFont())
        art.SetSelectedFont(self.GetSelectedFont())
        art.SetMeasuringFont(self.GetMeasuringFont())

        art = aui.aui_utilities.CopyAttributes(art, self)
        return art
