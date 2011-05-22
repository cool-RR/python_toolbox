# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `CuteFrame` class.

See its documentation for more information.
'''

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
        #style |= wx.WS_EX_CONTEXTHELP
        style = (wx.DEFAULT_FRAME_STYLE | wx.WS_EX_CONTEXTHELP) ^ \
             (wx.RESIZE_BORDER | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX)
        wx.Frame.__init__(self, parent=parent, id=id, title=title,
                          pos=pos, size=size, style=style, name=name)
        CuteTopLevelWindow.__init__(self, parent=parent, id=id, title=title,
                                    pos=pos, size=size, style=style, na\me=name)