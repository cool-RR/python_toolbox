# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.


import wx
wx.Dialog.ShowModal
class CuteDialog(wx.Dialog):
    def ShowModal(self):
        if wx.Platform == '__WXMAC__':
            wx.CallAfter(lambda: self.Centre(wx.BOTH))
        return super(CuteDialog, self).ShowModal()
    