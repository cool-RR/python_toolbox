import wx

from garlicsim.general_misc import caching
from garlicsim_wx.general_misc import color_tools
from garlicsim_wx.general_misc import wx_tools


@caching.cache()
def get_error_background_color():
    red = wx.Colour(255, 0, 0)
    return wx_tools.mix_wx_color(0.2, red, wx.Colour(255, 255, 255))
