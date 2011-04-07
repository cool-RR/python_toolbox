# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Monkeypatches `wx` to politely tell us that `wx` objects are non-pickleable.
'''

import wx
if not hasattr(wx.Object, '_is_atomically_pickleable'):
    wx.Object._is_atomically_pickleable = False