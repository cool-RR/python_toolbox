# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

import wx

from python_toolbox.wx_tools.widgets.cute_control import CuteControl

class CuteHiddenButton(wx.Button, CuteControl):
    def __init__(self, parent, *args, **kwargs):
        ''' '''
        wx.Button.__init__(self, parent, *args, **kwargs)
        self.Hide()