# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `SimpackInfoPanel` class.

See its documentation for more information.
'''

import wx

from garlicsim_wx.widgets.general_misc.cute_panel import CutePanel

from .name_display import NameDisplay


class SimpackInfoPanel(CutePanel):
    def __init__(self, simpack_selection_dialog):
        self.simpack_selection_dialog = simpack_selection_dialog
        CutePanel.__init__(self, simpack_selection_dialog)
        self.SetBackgroundColour(wx.NamedColour('blue'))
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.name_display = NameDisplay(self)
        self.sizer.Add(self.name_display,
                       proportion=0,
                       flag=(wx.ALIGN_RIGHT | wx.BOTTOM),
                       border=2)
        
        self.SetSizer(self.sizer)
        self.Layout()