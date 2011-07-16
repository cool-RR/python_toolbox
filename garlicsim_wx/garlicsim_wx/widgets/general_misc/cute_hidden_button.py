# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `CuteHiddenButton` class.

See its documentation for more information.
'''

import wx

from garlicsim_wx.widgets.general_misc.cute_control import CuteControl

class CuteHiddenButton(wx.Button, CuteControl):
    def __init__(self, parent, *args, **kwargs):
        ''' '''
        wx.Button.__init__(self, parent, *args, **kwargs)
        self.Hide()