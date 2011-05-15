# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''

menu_keys = [Key(wx.WXK_MENU), Key(wx.WXK_WINDOWS_MENU),
             Key(wx.WXK_F10, shift=True)]
'''Keys used for raising a context menu.'''

back_keys = (
    Key(ord('['), cmd=True),
    Key(wx.WXK_LEFT, cmd=True)
    ) if is_mac else (
        Key(wx.WXK_LEFT, alt=True),
    )

back_key_string = u'\u2318\u00ab' if is_mac else u'Alt-\u00ab'

forward_keys = (
    Key(ord(']'), cmd=True),
    Key(wx.WXK_RIGHT, cmd=True)
    ) if is_mac else (
        Key(wx.WXK_RIGHT, alt=True),
    )

forward_key_string = u'\u2318\u00bb' if is_mac else u'Alt-\u00bb'
