# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines colors for use in `ArgumentsControl`.'''

import wx

from garlicsim.general_misc import caching
from garlicsim_wx.general_misc import color_tools
from garlicsim_wx.general_misc import wx_tools


@caching.cache()
def get_error_background_color():
    '''Get the background color of a text control which has invalid input.'''
    red = wx.Colour(255, 0, 0)
    return wx_tools.colors.mix_wx_color(0.2, red, wx.Colour(255, 255, 255))
