# Copyright 2009-2011 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the `ErrorDialog` class.

See its documentation for more details.
'''

import wx

from garlicsim_wx.widgets.general_misc.cute_dialog import CuteDialog


class ErrorDialog(wx.MessageDialog, CuteDialog):
    '''Dialog showing error message with an error icon.'''
    def __init__(self, parent, message, caption='Error'):
        wx.MessageDialog.__init__(self, parent, message, caption,
                                  wx.OK | wx.ICON_ERROR)
        CuteDialog.__init__(self, skip_dialog_init=True)
        