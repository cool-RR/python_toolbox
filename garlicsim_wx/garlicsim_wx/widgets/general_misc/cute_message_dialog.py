# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `CuteMessageDialog` class.

See its documentation for more details.
'''

import wx

from garlicsim_wx.widgets.general_misc.cute_dialog import CuteDialog


class CuteMessageDialog(wx.MessageDialog, CuteDialog):
    '''blocktododoc'''
    def __init__(self, parent, message, caption='Message', style=wx.OK):
        wx.MessageDialog.__init__(self, parent, message, caption,
                                  style=style)
        CuteDialog.__init__(self, skip_wx_init=True)
        self.ExtraStyle &= ~wx.FRAME_EX_CONTEXTHELP
        