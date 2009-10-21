# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

from history_test import *

try:
    import wx
    wx_installed = True
except ImportError:
    wx_installed = False

if wx_installed:
    from history_test_gui import *