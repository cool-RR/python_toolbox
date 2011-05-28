# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `CuteFileDialog` class.

See its documentation for more info.
'''

import wx

from .cute_dialog import CuteDialog


class CuteFileDialog(CuteDialog, wx.FileDialog):
    '''
    An improved `wx.FileDialog`.
    
    The advantages of this class over `wx.FileDialog`:
    
      - blocktododoc
      - Other advantages given by `CuteDialog`
    
    '''
    
    def __init__(self, *args, **kwargs):
        wx.FileDialog.__init__(self, *args, **kwargs)
        CuteDialog.__init__(self, *args, **kwargs)
        self.ExtraStyle &= ~wx.FRAME_EX_CONTEXTHELP
        
    
    @classmethod # blocktodo: Use everywhere I can, document
    def create_show_modal_and_get_path(cls, *args, **kwargs):
        dialog = cls(*args, **kwargs)
        try:
            result = dialog.ShowModal()
        finally:
            dialog.Destroy()
        return dialog.GetPath() if result == wx.ID_OK else None
            