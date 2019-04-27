# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

import webbrowser

import wx.html

from python_toolbox.wx_tools.widgets.cute_window import CuteWindow


class CuteHtmlWindow(wx.html.HtmlWindow, CuteWindow):

    event_modules = wx.html

    def __init__(self, parent, id=-1, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.html.HW_DEFAULT_STYLE,
                 name=wx.html.HtmlWindowNameStr):
        wx.html.HtmlWindow.__init__(self, parent=parent, id=id, pos=pos,
                                    size=size, style=style, name=name)
        self.bind_event_handlers(CuteHtmlWindow)


    def _on_html_link_clicked(self, event):
        webbrowser.open_new_tab(
            event.GetLinkInfo().GetHref()
        )