# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `VersionDisplay` class.

See its documentation for more information.
'''

import wx

from garlicsim_wx.general_misc import wx_tools
from garlicsim_wx.widgets.general_misc.cute_static_text import CuteStaticText


class VersionDisplay(CuteStaticText):
    '''Static text showing the version number of the simpack, if one exists.'''
    
    def __init__(self, technical_details_bar):
        '''
        Construct the `VersionDisplay`, with `technical_details_bar` as parent.
        '''
        self.technical_details_bar = technical_details_bar
        CuteStaticText.__init__(self, technical_details_bar)
        self.HelpText = 'The version number of the currently-selected simpack.'
        
        # We want to write in a text which is slightly faint, because the
        # version is relatively non-important information:
        self.ForegroundColour = wx_tools.colors.mix_wx_color(
            0.5,
            self.ForegroundColour,
            self.BackgroundColour
        )
        
    def refresh(self):
        '''
        Display the version of the selected simpack-metadata if one exists.
        '''
        simpack_metadata = self.technical_details_bar.simpack_info_panel.\
                                      simpack_selection_dialog.simpack_metadata
        if (simpack_metadata is None) or (not simpack_metadata.version):
            self.Label = ''
        else:
            self.Label = 'Version %s' % simpack_metadata.version