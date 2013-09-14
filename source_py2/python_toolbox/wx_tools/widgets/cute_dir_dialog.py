# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `CuteDirDialog` class.

See its documentation for more info.
'''

import wx

from python_toolbox.wx_tools.cursors import CursorChanger
from .cute_dialog import CuteDialog


class CuteDirDialog(CuteDialog, wx.DirDialog):
    '''
    An improved `wx.DirDialog`.
    
    The advantages of this class over `wx.DirDialog`:
    
      - A class method `.create_show_modal_and_get_path` for quick usage.
      - Other advantages given by `CuteDialog`.
    
    '''
    
    def __init__(self, parent, message=wx.DirSelectorPromptStr, 
                 defaultPath=wx.EmptyString, style=wx.DD_DEFAULT_STYLE,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 name=wx.DirDialogNameStr):
        wx.DirDialog.__init__(self, parent, message, defaultPath, style, pos,
                              size, name)
        CuteDialog.__init__(self, parent, -1, style=style, size=size, pos=pos,
                            skip_wx_init=True)
        self.ExtraStyle &= ~wx.FRAME_EX_CONTEXTHELP
        
    
    @classmethod
    def create_show_modal_and_get_path(cls, *args, **kwargs):
        '''
        Create `CuteDirDialog`, show it, and get the path that was selected.
        
        Returns `None` if "Cancel" was pressed.
        '''
        dialog = cls(*args, **kwargs)
        try:
            result = dialog.ShowModal()
        finally:
            dialog.Destroy()
        return dialog.GetPath() if result == wx.ID_OK else None
            