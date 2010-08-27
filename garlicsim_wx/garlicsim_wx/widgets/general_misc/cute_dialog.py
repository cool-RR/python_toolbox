# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the CuteDialog class.

See its documentation for more info.
'''

import wx

from garlicsim_wx.general_misc import wx_tools


class CuteDialog(wx.Dialog):
    '''Dialog that works around a Mac bug by centering itself on the screen.'''
    def __init__(self, *args, **kwargs):
        wx.Dialog.__init__(self, *args, **kwargs)
        self.SetBackgroundColour(wx_tools.get_background_color())
        
    def ShowModal(self):
        if wx.Platform == '__WXMAC__':
            wx.CallAfter(lambda: self.Centre(wx.BOTH))
        return super(CuteDialog, self).ShowModal()
    