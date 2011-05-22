# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''

import wx

from .cute_top_level_window import CuteTopLevelWindow

class CuteFrame(wx.Frame, CuteTopLevelWindow):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        CuteTopLevelWindow.__init__(self, *args, **kwargs)