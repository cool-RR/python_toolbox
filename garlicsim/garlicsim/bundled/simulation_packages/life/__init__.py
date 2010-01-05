# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
A simulation package for Conway's Game of Life.
'''

from life import *

wx_installed=False
try:
    import wx
    wx_installed=True
except ImportError:
    pass

if wx_installed:
    from life_wx import *
    

class Meta:
    deterministic = 2
    scalar_state_functions = [live_cells]
    scalar_history_function = [changes]
    