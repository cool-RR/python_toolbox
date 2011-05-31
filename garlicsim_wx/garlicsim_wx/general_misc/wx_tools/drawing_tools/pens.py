# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''

import wx

from garlicsim.general_misc import caching


is_mac = (wx.Platform == '__WXMAC__')
is_gtk = (wx.Platform == '__WXGTK__')
is_win = (wx.Platform == '__WXMSW__')


@caching.cache()
def get_selection_pen():
    ''' '''
    if is_mac:
        return 1/0 #blocktododoc implement
    else:
        pen = wx.Pen(wx.Color(0, 0, 0),
                     1,
                     wx.USER_DASH)
        pen.SetDashes([1, 4])
        return pen
    
    