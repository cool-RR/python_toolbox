# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `CuteFileDialog` class.

See its documentation for more info.
'''

import wx

from python_toolbox.wx_tools.cursors import CursorChanger
from .cute_dialog import CuteDialog


class CuteFileDialog(CuteDialog, wx.FileDialog):
    '''
    An improved `wx.FileDialog`.
    
    The advantages of this class over `wx.FileDialog`:
    
      - A class method `.create_show_modal_and_get_path` for quick usage.
      - Other advantages given by `CuteDialog`
    
    '''
    
    def __init__(self, parent, message=wx.FileSelectorPromptStr, 
                 defaultDir=wx.EmptyString, defaultFile=wx.EmptyString,
                 wildcard=wx.FileSelectorDefaultWildcardStr, 
                 style=wx.FD_DEFAULT_STYLE, pos=wx.DefaultPosition):
        wx.FileDialog.__init__(self, parent, message, defaultDir, defaultFile,
                               wildcard, style, pos)
        CuteDialog.__init__(self, parent, -1, style=style, skip_wx_init=True)
        self.ExtraStyle &= ~wx.FRAME_EX_CONTEXTHELP
        
    
    @classmethod
    def create_show_modal_and_get_path(cls, *args, **kwargs):
        '''
        Create `CuteFileDialog`, show it, and get the path that was selected.
        
        Returns `None` if "Cancel" was pressed.
        '''
        dialog = cls(*args, **kwargs)
        try:
            result = dialog.ShowModal()
        finally:
            dialog.Destroy()
        return dialog.GetPath() if result == wx.ID_OK else None
            