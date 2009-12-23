# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
A simpack for simulations in Queueing Theory.
'''

from queue import *

wx_installed = False
try:
    import wx
    wx_installed = True
except ImportError:
    pass

if wx_installed:
    from queue_wx import *