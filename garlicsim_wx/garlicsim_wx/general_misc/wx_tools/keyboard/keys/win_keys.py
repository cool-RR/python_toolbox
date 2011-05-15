# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''This module defines Windows-specific keys.'''

from garlicsim.general_misc.wx_tools.keyboard import Key


back_keys = (
    Key(wx.WXK_LEFT, alt=True),
)

back_key_string = u'Alt-\u00ab'

forward_keys = (
    Key(wx.WXK_RIGHT, alt=True),
)

forward_key_string = u'Alt-\u00bb'