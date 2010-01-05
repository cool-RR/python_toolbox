# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''A simulation package for Conway's Game of Life.'''

from life import *

class Meta(object):
    deterministic = 2
    scalar_state_functions = [live_cells]
    scalar_history_function = [changes]

wx_installed = False
try:
    import wx
    wx_installed = True
except ImportError:
    pass

if wx_installed:
    from life_wx import *
    
    class Meta_wx(object):
        seek_bar_graphs = [live_cells, changes]
    


    
