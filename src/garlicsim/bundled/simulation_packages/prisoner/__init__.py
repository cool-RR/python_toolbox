# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

from prisoner import *

wx_installed=False
try:
    import wx
    wx_installed=True
except ImportError:
    pass

if wx_installed:
    from prisoner_gui import *