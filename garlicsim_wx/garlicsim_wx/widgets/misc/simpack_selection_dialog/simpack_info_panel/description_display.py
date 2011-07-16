# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `DescriptionDisplay` class.

See its documentation for more information.
'''

import urlparse

import docutils.core
import wx

from garlicsim.general_misc import caching
from garlicsim_wx.widgets.general_misc.cute_html_window import CuteHtmlWindow
from garlicsim_wx.general_misc import wx_tools


@caching.cache()
def get_background_html_color():
    if wx_tools.is_mac:
        return '#e0e0e0' # Hard-coded color of Mac static box.
    else:
        return wx_tools.colors.wx_color_to_html_color(
            wx_tools.colors.get_background_color(),
        )

    
@caching.cache()
def get_foreground_html_color():
    return wx_tools.colors.wx_color_to_html_color(
        wx_tools.colors.get_foreground_color(),
    )


@caching.cache()
def tag_to_html(tag):
    return '<a href="%s">%s</a>' % (tag, tag)


@caching.cache()
def tags_to_html(tags):
    return '''
        <table id="tags">
          <tr>
            <td>
              <b>
                Tags:
              </b> 
            </td>
            <td>
              %s
            </td>
          </tr>
        </table>
            ''' % (
        ', '.join(tag_to_html(tag) for tag in tags),
                ) if tags else ''

@caching.cache()
def simpack_metadata_to_html(simpack_metadata):
    parsed_rst = docutils.core.publish_parts(simpack_metadata.description,
                                             writer_name='html')['body']
    return '''
          <body bgcolor="%s" text="%s">
            %s
            <div id="description">
              %s
            </div>
          </body>
        </html>
        ''' % (
            get_background_html_color(),
            get_foreground_html_color(),
            tags_to_html(simpack_metadata.tags),
            parsed_rst
        )


class DescriptionDisplay(CuteHtmlWindow):

    def __init__(self, simpack_info_panel):
        self.simpack_info_panel = simpack_info_panel
        CuteHtmlWindow.__init__(
            self,
            simpack_info_panel,
            style=(wx.html.HW_DEFAULT_STYLE)
        )
        self.HelpText = 'A description of the currently-selected simpack.'
        self.Hide()
        self.bind_event_handlers(DescriptionDisplay)
        
        
    def refresh(self):
        simpack_metadata = \
            self.simpack_info_panel.simpack_selection_dialog.simpack_metadata
        if simpack_metadata is not None:
            self.Show()
            self.SetPage(
                simpack_metadata_to_html(
                    simpack_metadata
                )
            )
        else: # simpack_metadata is None
            self.Hide()
            
        
    def _on_html_link_clicked(self, event):
        target = event.GetLinkInfo().GetHref()        
        parsed_target = urlparse.urlparse(target)
        if not parsed_target.scheme: # Link to tag
            simpack_selection_dialog = \
                               self.simpack_info_panel.simpack_selection_dialog
            filter_box = simpack_selection_dialog.navigation_panel.filter_box
            filter_box.SetFocus()
            filter_box.Value = target
            simpack_selection_dialog.simpack_tree.SetFocus()
            simpack_selection_dialog.simpack_tree.reload_tree(
                ensure_simpack_selected=True
            )
            
        else: # Link to web address, let parent widget open in browser:
            event.Skip()
            