# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
A simulation package for testing garlicsim's ability to handle
history-dependent simulations.
'''

from history_test import *

try:
    import wx
    wx_installed = True
except ImportError:
    wx_installed = False

if wx_installed:
    from history_test_wx import *