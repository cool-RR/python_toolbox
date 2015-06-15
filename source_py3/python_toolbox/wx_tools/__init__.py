# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines various tools for wxPython.'''

import wx


is_mac = (wx.Platform == '__WXMAC__')
is_gtk = (wx.Platform == '__WXGTK__')
is_win = (wx.Platform == '__WXMSW__')


from . import colors
from . import keyboard
from . import window_tools
from . import bitmap_tools
from . import cursors
from . import event_tools
from . import generic_bitmaps
from . import drawing_tools
from . import timing
