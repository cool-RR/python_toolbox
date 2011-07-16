# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `DescriptionDisplay` class.

See its documentation for more information.
'''

import urlparse

import wx

from garlicsim.general_misc import caching
from garlicsim_wx.widgets.general_misc.cute_html_window import CuteHtmlWindow
from garlicsim_wx.general_misc import wx_tools
from garlicsim_wx.general_misc import rst_tools


@caching.cache()
def get_background_html_color():
    '''Get the background color as an html color string.'''
    if wx_tools.is_mac:
        return '#e0e0e0' # Hard-coded color of Mac static box.
    else:
        return wx_tools.colors.wx_color_to_html_color(
            wx_tools.colors.get_background_color(),
        )

    
@caching.cache()
def get_foreground_html_color():
    '''Get the foreground color as an html color string.'''
    return wx_tools.colors.wx_color_to_html_color(
        wx_tools.colors.get_foreground_color(),
    )


@caching.cache()
def tag_to_html(tag):
    '''Show a simpack tag as an HTML ling.'''
    return '<a href="%s">%s</a>' % (tag, tag)


@caching.cache()
def tags_to_html(tags):
    '''Convert a simpack's list of tags to a table of links in HTML.'''
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
    '''Show a simpack-metadata's description and tags as an HTML document.'''
    return '''
        <html>
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
            rst_tools.rst_to_html(simpack_metadata.description or '')
        )


class DescriptionDisplay(CuteHtmlWindow):
    '''HTML window showing the simpack's description and tags.'''
    
    def __init__(self, simpack_info_panel):
        '''Construct the `DescriptionDisplay`.'''
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
        '''Update to show the description of the currently-selected simpack.'''
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
        # When clicking a link to a web address, we should open a browser; when
        # clicking a link to a tag, we should filter simpacks by that tag.
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
            