# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `TechnicalDetailsBar` class.

See its documentation for more information.
'''

import wx

from garlicsim_wx.widgets.general_misc.cute_panel import CutePanel

from .version_display import VersionDisplay
from .code_link import CodeLink


class TechnicalDetailsBar(CutePanel):
    def __init__(self, simpack_info_panel):
        ''' '''
        self.simpack_info_panel = simpack_info_panel
        CutePanel.__init__(self, simpack_info_panel)
        self.BackgroundColour = self.simpack_info_panel.static_box.\
                                                               BackgroundColour
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.version_display = VersionDisplay(self)
        self.sizer.Add(self.version_display,
                       proportion=0,
                       flag=(wx.ALIGN_CENTER_VERTICAL | wx.RIGHT),
                       border=5)
        
        self.code_link = CodeLink(self)
        self.sizer.Add(self.code_link,
                       proportion=0,
                       flag=wx.ALIGN_CENTER_VERTICAL)
        
        self.SetSizer(self.sizer)
        self.Layout()
        
        
    def refresh(self):
        self.version_display.refresh()
        self.code_link.refresh()
        self.Layout
        