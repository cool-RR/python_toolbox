# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `CodeLink` class.

See its documentation for more information.
'''

import wx

from garlicsim_wx.general_misc import wx_tools
from garlicsim_wx.widgets.general_misc.cute_hyper_link import CuteHyperLink


class CodeLink(CuteHyperLink):
    def __init__(self, technical_details_bar):
        ''' '''
        self.technical_details_bar = technical_details_bar
        CuteHyperLink.__init__(self, technical_details_bar, label=)
        self.ForegroundColour = wx_tools.colors.mix_wx_color(
            0.333,
            self.ForegroundColour,
            self.BackgroundColour
        )
        
    def refresh(self):
        simpack_metadata = self.technical_details_bar.simpack_info_panel.\
                                      simpack_selection_dialog.simpack_metadata
        self.SetLabel(('Version %s' % simpack_metadata.version) if
                      simpack_metadata is not None else '')
        
        