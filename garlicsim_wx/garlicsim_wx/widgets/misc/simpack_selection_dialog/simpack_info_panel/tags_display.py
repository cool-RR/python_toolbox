# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `TagsDisplay` class.

See its documentation for more information.
'''

import wx

from garlicsim.general_misc import caching
from garlicsim_wx.widgets.general_misc.cute_panel import CutePanel
from garlicsim_wx.general_misc import wx_tools


class TagsDisplay(CutePanel):

    def __init__(self, simpack_info_panel):
        self.simpack_info_panel = simpack_info_panel
        CutePanel.__init__(self, simpack_info_panel)
        self.Hide()
        
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.sizer)
                
        self.tags_static_text = wx.StaticText(self, label='&Tags:')
        self.sizer.Add(self.tags_static_text,
                       proportion=0,
                       flag=(wx.ALIGN_TOP | wx.RIGHT),
                       border=2)
        

        
        
    def refresh(self):
        simpack_metadata = \
            self.simpack_info_panel.simpack_selection_dialog.simpack_metadata
        if simpack_metadata is not None:
            self.Show()
            self.Layout()
        else: # simpack_metadata is None
            self.Hide()
            
        