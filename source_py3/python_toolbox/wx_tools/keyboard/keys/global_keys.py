# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines keys that work on all operating systems.'''

import wx

from ..key import Key


menu_keys = [Key(wx.WXK_MENU), Key(wx.WXK_WINDOWS_MENU),
             Key(wx.WXK_F10, shift=True)]
'''Keys used for raising a context menu.'''
# todo: explode into OSes and get the Mac one. (I think it's Function-Ctrl-5 or
# something.)

enter_keys = [Key(wx.WXK_RETURN), Key(wx.WXK_NUMPAD_ENTER)]