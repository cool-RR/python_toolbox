# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

import wx

from python_toolbox.wx_tools.cursors import CursorChanger
from python_toolbox import context_management

from python_toolbox.wx_tools.widgets.cute_window import CuteWindow


class CuteDialogType(type(CuteWindow)):
    def __call__(self, parent, *args, **kwargs):
        context_manager = \
            CursorChanger(parent, wx.CURSOR_WAIT) if parent else \
            context_management.BlankContextManager()
        with context_manager:
            return type.__call__(self, parent, *args, **kwargs)