# Copyright 2009-2011 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the `CuteDialog` class.

See its documentation for more info.
'''

import wx

from garlicsim_wx.general_misc import wx_tools


class CuteDialog(wx.Dialog):
    '''Improved dialog.'''
    def __init__(self, *args, **kwargs):
        if not kwargs.pop('skip_dialog_init', False):
            wx.Dialog.__init__(self, *args, **kwargs)
        self.SetBackgroundColour(wx_tools.get_background_color())

        
    def ShowModal(self):
        self.Centre(wx.BOTH)
        return super(CuteDialog, self).ShowModal()
    
    
    @classmethod
    def create_show_modal_and_destroy(cls, *args, **kwargs):
        dialog = cls(*args, **kwargs)
        try:
            result = dialog.ShowModal()
        finally:
            dialog.Destroy()
        return result