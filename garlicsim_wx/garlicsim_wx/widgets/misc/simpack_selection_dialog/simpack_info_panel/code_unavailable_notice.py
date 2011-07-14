# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `CodeUnavailableNotice` class.

See its documentation for more information.
'''

import wx

from garlicsim_wx.general_misc import wx_tools
from garlicsim_wx.widgets.general_misc.cute_static_text import CuteStaticText

base_help_text = "Sorry, the source code for this simpack is not available."

class CodeUnavailableNotice(CuteStaticText):
    def __init__(self, code_link):
        ''' '''
        self.code_link = code_link
        CuteStaticText.__init__(self,
                                code_link,
                                label='(Code unavailable)')
        self.HelpText = base_help_text
        self.SetToolTipString(self.HelpText)
        self.ForegroundColour = wx_tools.colors.mix_wx_color(
            0.5,
            self.ForegroundColour,
            self.BackgroundColour
        )
        
    def set_reason(self, reason):
        self.HelpText = base_help_text + reason
        self.SetToolTipString(self.HelpText)