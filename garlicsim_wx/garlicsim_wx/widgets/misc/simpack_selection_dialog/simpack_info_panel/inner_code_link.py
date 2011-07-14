# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `InnerCodeLink` class.

See its documentation for more information.
'''

import os.path

import wx

from garlicsim.general_misc import os_tools
from garlicsim.general_misc import sys_tools
from garlicsim_wx.general_misc import wx_tools
from garlicsim_wx.widgets.general_misc.cute_hyperlink_ctrl \
                                                       import CuteHyperlinkCtrl


class InnerCodeLink(CuteHyperlinkCtrl):
    
    def __init__(self, code_link):
        ''' '''
        self.code_link = code_link
        CuteHyperlinkCtrl.__init__(self, code_link, label='Show code')
        self.HelpText = ("Click to open the folder with currently-selected "
                         "simpack's code.")
        if wx_tools.is_gtk:
            self.BackgroundColour = self.Parent.BackgroundColour
        self.VisitedColour = self.HoverColour = self.NormalColour
        self.bind_event_handlers(InnerCodeLink)
        self.Hide()
        
        
    def _on_hyperlink(self, event):
        simpack_metadata = \
            self.code_link.technical_details_bar.simpack_info_panel.\
                                      simpack_selection_dialog.simpack_metadata
        assert simpack_metadata is not None
        folder_path = \
            os.path.split(simpack_metadata._tasted_simpack.__file__)[0]
        os_tools.start_file(folder_path)
        
        