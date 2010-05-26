# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the CuteTimer class.

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
        