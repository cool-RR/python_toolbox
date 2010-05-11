
import wx

from garlicsim_wx.general_misc import cute_base_timer


__all__ = ['CuteTimer']


class CuteTimer(wx.Timer, cute_base_timer.CuteBaseTimer):
    # todo: Should use PyTimer?
    def __init__(self, parent=None, id=wx.ID_ANY):
        wx.Timer.__init__(self, parent, id)
        CuteBaseTimer.__init__(self, parent)
        