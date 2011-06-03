# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''

import wx

class CuteHiddenButton(wx.Button): # blocktodo: inherit from CuteControl?
    def __init__(self, parent, *args, **kwargs):
        ''' '''
        wx.Button.__init__(self, parent, *args, **kwargs)
        self.Hide()