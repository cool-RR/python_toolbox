# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''This module defines Windows-specific keys.'''

import wx

from ..key import Key


back_keys = (
    Key(wx.WXK_LEFT, alt=True),
)

back_key_string = u'Alt-\u00ab'

forward_keys = (
    Key(wx.WXK_RIGHT, alt=True),
)

forward_key_string = u'Alt-\u00bb'