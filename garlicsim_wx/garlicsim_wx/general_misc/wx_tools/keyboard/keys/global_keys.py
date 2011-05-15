# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines keys that work on all operating systems.'''

from garlicsim.general_misc.wx_tools.keyboard import Key


menu_keys = [Key(wx.WXK_MENU), Key(wx.WXK_WINDOWS_MENU),
             Key(wx.WXK_F10, shift=True)]
'''Keys used for raising a context menu.'''
# blocktodo: explode into OSes cause Mac is probably different

