# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `CuteTimer` class.

See its documentation for more information.
'''

import wx

from garlicsim_wx.general_misc import cute_base_timer


__all__ = ['CuteTimer']


class CuteTimer(wx.Timer, cute_base_timer.CuteBaseTimer):
    '''A wx.Timer that allows central stopping.'''
    # todo: Should use PyTimer?
    def __init__(self, parent=None, id=wx.ID_ANY):
        wx.Timer.__init__(self, parent, id)
        cute_base_timer.CuteBaseTimer.__init__(self, parent)
        