# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

import wx

from .cute_top_level_window import CuteTopLevelWindow


class CuteFrame(wx.Frame, CuteTopLevelWindow):
    '''
    An improved `wx.Frame`.
    
    See `CuteTopLevelWindow` for what this class gives over `wx.Frame`.
    '''
    def __init__(self, parent, id=-1, title=wx.EmptyString,
                 pos=wx.DefaultPosition, size=wx.DefaultSize, 
                 style=wx.DEFAULT_FRAME_STYLE, name=wx.FrameNameStr):
        wx.Frame.__init__(self, parent=parent, id=id, title=title,
                          pos=pos, size=size, style=style, name=name)
        CuteTopLevelWindow.__init__(self, parent=parent, id=id, title=title,
                                    pos=pos, size=size, style=style, name=name)