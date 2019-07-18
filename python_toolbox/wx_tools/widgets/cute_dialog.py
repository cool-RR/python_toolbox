# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `CuteDialog` class.

See its documentation for more info.
'''

import wx

from .cute_top_level_window import CuteTopLevelWindow
from .cute_dialog_type import CuteDialogType


class CuteDialog(wx.Dialog, CuteTopLevelWindow, metaclass=CuteDialogType):
    '''
    An improved `wx.Dialog`.

    The advantages of this class over `wx.Dialog`:

      - `ShowModal` centers the dialog on its parent, which sometimes doesn't
        happen by itself on Mac.
      - A `create_and_show_modal` class method.
      - A "context help" button on Windows only.
      - Other advantages given by `CuteTopLevelWindow`

    '''


    def __init__(self, *args, **kwargs):
        if not kwargs.pop('skip_wx_init', False):
            wx.Dialog.__init__(self, *args, **kwargs)
        CuteTopLevelWindow.__init__(self, *args, **kwargs)
        self.ExtraStyle |= wx.FRAME_EX_CONTEXTHELP


    def ShowModal(self):
        self.Centre(wx.BOTH)
        return super().ShowModal()


    @classmethod
    def create_and_show_modal(cls, parent, *args, **kwargs):
        dialog = cls(parent, *args, **kwargs)
        try:
            result = dialog.ShowModal()
        finally:
            dialog.Destroy()
        return result