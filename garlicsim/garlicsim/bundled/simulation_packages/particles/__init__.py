# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
tododoc
'''

from particles import *

wx_installed=False
try:
    import wx
    wx_installed=True
except ImportError:
    pass

if wx_installed:
    from particles_wx import *