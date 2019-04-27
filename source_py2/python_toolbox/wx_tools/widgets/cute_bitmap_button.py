# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

import wx

from python_toolbox.wx_tools.widgets.cute_button import CuteButton


class CuteBitmapButton(wx.BitmapButton, CuteButton):
    def __init__(self, parent, id=-1, bitmap=wx.NullBitmap,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.BU_AUTODRAW, validator=wx.DefaultValidator,
                 name=wx.ButtonNameStr, bitmap_disabled=None, tool_tip=None,
                 help_text=None):

        wx.BitmapButton.__init__(self, parent=parent, id=id, bitmap=bitmap,
                                 pos=pos, size=size, style=style,
                                 validator=validator, name=name)
        if bitmap_disabled is not None:
            self.SetBitmapDisabled(bitmap_disabled)
        self.set_tool_tip_and_help_text(tool_tip, help_text)
