# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `CuteTopLevelWindow` class.

See its documentation for more information.
'''

import wx

from .cute_window import CuteWindow


class CuteTopLevelWindow(wx.TopLevelWindow, CuteWindow):
    '''
    An improved `wx.TopLevelWindow`.
    
    The advantages of this class over `wx.TopLevelWindow`:
    
      - A good background color.
      - Advantages given by `CuteWindow`
    
    '''
    def __init__(self, *args, **kwargs):
        self.set_good_background_color()