# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

import wx

from python_toolbox.wx_tools.widgets.cute_control import CuteControl


class CuteHyperlinkCtrl(wx.HyperlinkCtrl, CuteControl):
    ''' '''
    def __init__(self, parent, id=-1, label='', url='', pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.HL_DEFAULT_STYLE,
                 name=wx.HyperlinkCtrlNameStr):

        wx.HyperlinkCtrl.__init__(
            self, parent=parent, id=id, label=label, url=url, pos=pos,
            size=size, style=style, name=name
        )
        
    
    