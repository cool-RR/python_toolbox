# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `DescriptionDisplay` class.

See its documentation for more information.
'''

import re

import docutils.parsers.rst
import docutils.utils
import docutils.core
import wx

from garlicsim.general_misc import caching
from garlicsim_wx.widgets.general_misc.cute_html_window import CuteHtmlWindow
from garlicsim_wx.general_misc import wx_tools


@caching.cache()
def get_background_html_color():
    return wx_tools.colors.wx_color_to_html_color(
        wx_tools.colors.mix_wx_color(
            0.8,
            wx_tools.colors.get_background_color(),
            wx.NamedColour('yellow')
        )
    )
    
# blocktodo: probably need foreground color too


@caching.cache()
def tag_to_html(tag):
    return '''<a href="%s">%s</a>''' % (tag, tag)

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
        <br />
            ''' % (
        ', '.join(tag_to_html(tag) for tag in tags),
                ) if tags else ''

@caching.cache()
def simpack_metadata_to_html(simpack_metadata):
    #parser = docutils.parsers.rst.Parser()
    #document = docutils.utils.new_document(None)
    #document.settings.tab_width = 4
    #parser.parse(simpack_metadata.description, document)
    x = docutils.core.publish_parts(simpack_metadata.description,
                                     writer_name='html')['body']
    
    
    return '''
        <html>
          <head>
            <style type="text/css">
              a:hover {
                color: black;
              }
            </style>
          </head>
          <body bgcolor="%s" color="%s">
            %s
            <div id="description">
              %s
            </div>
          </body>
        </html>
        ''' % \
            (
                get_background_html_color(),
                'black',
                tags_to_html(simpack_metadata.tags),
                x #simpack_metadata.description,
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
            self.SetPage(
                simpack_metadata_to_html(
                    simpack_metadata
                )
            )
        else: # simpack_metadata is None
            self.Hide()
            
        