# Copyright 2009-2011 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Monkeypatches `wx` to politely tell us that `wx` objects are non-pickleable.
'''

import wx
if not hasattr(wx.Object, '_is_atomically_pickleable'):
    wx.Object._is_atomically_pickleable = False