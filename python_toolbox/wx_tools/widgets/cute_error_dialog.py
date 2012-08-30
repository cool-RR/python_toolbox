# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `CuteErrorDialog` class.

See its documentation for more details.
'''

import wx

from python_toolbox.wx_tools.widgets.cute_dialog import CuteDialog


class CuteErrorDialog(wx.MessageDialog, CuteDialog):
    '''Dialog showing error message with an error icon.'''
    def __init__(self, parent, message, caption='Error',
                 style=(wx.OK | wx.ICON_ERROR)):
        wx.MessageDialog.__init__(self, parent, message, caption,
                                  style=style)
        CuteDialog.__init__(self, skip_wx_init=True)
        self.ExtraStyle &= ~wx.FRAME_EX_CONTEXTHELP
        