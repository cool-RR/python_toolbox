# Copyright 2009-2011 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''Defines colors for use in `ArgumentsControl`.'''

import wx

from garlicsim.general_misc import caching
from garlicsim_wx.general_misc import color_tools
from garlicsim_wx.general_misc import wx_tools


@caching.cache()
def get_error_background_color():
    '''Get the background color of a text control which has invalid input.'''
    red = wx.Colour(255, 0, 0)
    return wx_tools.mix_wx_color(0.2, red, wx.Colour(255, 255, 255))
