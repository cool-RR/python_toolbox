# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
This module defines the AuiTabArt class.

See its documentation for more info.
'''

import wx
from garlicsim_wx.general_misc.third_party import aui

class AuiTabArt(aui.AuiDefaultTabArt):
    '''A tab art provider.'''
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
