# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `TagsDisaply` class.

See its documentation for more information.
'''

import wx

from garlicsim.general_misc import caching
from garlicsim_wx.widgets.general_misc.cute_panel import CutePanel
from garlicsim_wx.general_misc import wx_tools


class TagsDisaply(CutePanel):

    def __init__(self, simpack_info_panel):
        self.simpack_info_panel = simpack_info_panel
        CutePanel.__init__(self, simpack_info_panel)
        
    def refresh(self):
        simpack_metadata = \
            self.simpack_info_panel.simpack_selection_dialog.simpack_metadata
        if simpack_metadata is not None:
            self.Show()
        else: # simpack_metadata is None
            self.Hide()
            
        