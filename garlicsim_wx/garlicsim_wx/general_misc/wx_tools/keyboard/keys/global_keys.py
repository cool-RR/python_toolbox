# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines keys that work on all operating systems.'''

import wx

from ..key import Key


menu_keys = [Key(wx.WXK_MENU), Key(wx.WXK_WINDOWS_MENU),
             Key(wx.WXK_F10, shift=True)]
'''Keys used for raising a context menu.'''
# blocktodo: explode into OSes cause Mac is probably different

enter_keys = [Key(wx.WXK_RETURN), Key(wx.WXK_NUMPAD_ENTER)]