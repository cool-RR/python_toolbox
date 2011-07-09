# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `Name` class.

See its documentation for more information.
'''

import wx

from garlicsim_wx.widgets.general_misc.cute_static_text import CuteStaticText



class NameDisplay(CuteStaticText):
    def __init__(self, simpack_info_panel):
        ''' '''
        self.simpack_info_panel = simpack_info_panel
        CuteStaticText.__init__(self, simpack_info_panel)
        self.SetFont(wx.Font(48, wx.NORMAL, wx.NORMAL, wx.NORMAL))
        self.simpack_info_panel.simpack_selection_dialog.\
                      simpack_metadata_changed_emitter.add_output(self.refresh)
        
    def refresh(self):
        simpack_metadata = self.simpack_info_panel.\
                                      simpack_selection_dialog.simpack_metadata
        self.SetLabel(simpack_metadata.name)
        