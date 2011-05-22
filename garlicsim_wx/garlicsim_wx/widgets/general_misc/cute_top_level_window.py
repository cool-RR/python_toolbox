# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''

import wx

from .cute_window import CuteWindow


class CuteTopLevelWindow(wx.TopLevelWindow, CuteWindow):
    def __init__(self, *args, **kwargs):
        self.ExtraStyle |= wx.FRAME_EX_CONTEXTHELP
        self.set_good_background_color()
        self.SetDoubleBuffered(True)