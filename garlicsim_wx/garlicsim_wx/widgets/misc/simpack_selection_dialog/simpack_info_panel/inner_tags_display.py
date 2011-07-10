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

    
# blocktodo: probably need foreground color too

@caching.cache()
def tag_to_html(tag):
    return '''<a href="%s">%s</a>''' % (tag, tag)


@caching.cache()
def tags_to_html(tags):
    return '''
        <html style="margin: 0px; padding: 0px;">
          <body bgcolor="%s" color="%s" style="margin: 0px; padding: 0px;">
            %s
          </body>
        </html>
    ''' % (
        wx_tools.colors.wx_color_to_html_color(
            wx_tools.colors.get_background_color()
        ),
        'black',
        ', '.join(tag_to_html(tag) for tag in tags)
    )


class InnerTagsDisplay(CuteHtmlWindow):

    def __init__(self, tags_display):
        self.tags_display = tags_display
        CuteHtmlWindow.__init__(
            self,
            tags_display,
            style=wx.html.HW_DEFAULT_STYLE
        )
        self.Hide()
        
    def refresh(self):
        simpack_metadata = self.tags_display.simpack_info_panel.\
                           simpack_selection_dialog.simpack_metadata
        if simpack_metadata is not None:
            self.Show()
            self.SetPage(tags_to_html(simpack_metadata.tags))
        else: # simpack_metadata is None
            self.Hide()
            
        