# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `CuteStaticText` class.

See its documentation for more info.
'''

import wx

from .cute_window import CuteWindow


class CuteStaticText(wx.StaticText, CuteWindow):
    '''


    '''
    def __init__(self, parent, id=-1, label=wx.EmptyString,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=0, name=wx.StaticTextNameStr, skip_wx_init=False):

        if not skip_wx_init:
            wx.StaticText.__init__(self, parent=parent, id=id, label=label,
                                   pos=pos, size=size, style=style, name=name)
        self.label = label
        self.bind_event_handlers(CuteStaticText)



