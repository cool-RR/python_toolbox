# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

import wx

from python_toolbox.wx_tools.widgets.cute_window import CuteWindow


class CutePanel(wx.Panel, CuteWindow):
    '''

    This class doesn't require calling its `__init__` when subclassing. (i.e.,
    you *may* call its `__init__` if you want, but it will do the same as
    calling `wx.Window.__init__`.)
    '''
