# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `DescriptionDisplay` class.

See its documentation for more information.
'''

import wx

from garlicsim.general_misc import caching
from garlicsim_wx.widgets.general_misc.cute_html_window import CuteHtmlWindow
from garlicsim_wx.general_misc import wx_tools


@caching.cache()
def get_background_html_color():
    return wx_tools.colors.wx_color_to_html_color(
        wx_tools.colors.mix_wx_color(
            0.7,
            wx_tools.colors.get_background_color(),
            wx.NamedColour('yellow')
        )
    )
    
# blocktodo: probably need foreground color too

@caching.cache()
def description_to_html(description):
    return '''
        <html>
          <body bgcolor="%s" color="%s">
            <font face="Georgia">
              %s
            </font>
          </body>
        </html>
        ''' % \
            (
                get_background_html_color(),
                'black',
                description
            )


class DescriptionDisplay(CuteHtmlWindow):

    def __init__(self, simpack_info_panel):
        self.simpack_info_panel = simpack_info_panel
        CuteHtmlWindow.__init__(
            self,
            simpack_info_panel,
            style=(wx.html.HW_DEFAULT_STYLE | wx.SUNKEN_BORDER)
        )
        self.Hide()
        
    def refresh(self):
        simpack_metadata = \
            self.simpack_info_panel.simpack_selection_dialog.simpack_metadata
        if simpack_metadata is not None:
            self.Show()
            self.SetPage(description_to_html(simpack_metadata.description))
        else: # simpack_metadata is None
            self.Hide()
            
        