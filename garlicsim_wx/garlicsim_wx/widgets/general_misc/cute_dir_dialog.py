# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `CuteDirDialog` class.

See its documentation for more info.
'''

import wx

from garlicsim_wx.general_misc.wx_tools.cursors import CursorChanger
from .cute_dialog import CuteDialog


class CuteDirDialog(CuteDialog, wx.DirDialog):
    '''
    An improved `wx.DirDialog`.
    
    The advantages of this class over `wx.DirDialog`:
    
      - blocktododoc
      - Other advantages given by `CuteDialog`
    
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
        
    
    @classmethod # blocktodo: Use everywhere I can, document
    def create_show_modal_and_get_path(cls, *args, **kwargs):
        dialog = cls(parent, *args, **kwargs)
        try:
            result = dialog.ShowModal()
        finally:
            dialog.Destroy()
        return dialog.GetPath() if result == wx.ID_OK else None
            