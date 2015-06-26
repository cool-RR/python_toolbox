# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''
Defines color-related tools.

This includes functions for getting general colors (e.g. background color) and
functions to convert between different respresentations of colors.
'''


from __future__ import division

import colorsys
import warnings

import wx

from python_toolbox import caching
from python_toolbox import color_tools


is_mac = (wx.Platform == '__WXMAC__')
is_gtk = (wx.Platform == '__WXGTK__')
is_win = (wx.Platform == '__WXMSW__')


@caching.cache()
def get_foreground_color():
    '''Get the default foreground color.'''    
    return wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENUTEXT)


@caching.cache()
def get_background_color():
    '''Get the default background color'''
    
    if is_win:
        # return wx.Colour(212, 208, 200)
        return wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENUBAR)
    elif is_mac:
        return wx.Colour(232, 232, 232)
    elif is_gtk:
        # Until `SYS_COLOUR_*` get their act togother, we're using Windows
        # colors for Linux.
        return wx.Colour(212, 208, 200)
    
    else:
        warnings.warn("Unidentified platform! It's neither '__WXGTK__', "
                      "'__WXMAC__' nor '__WXMSW__'. Things might not work "
                      "properly.")
        return wx.Colour(212, 208, 200)
    
    
@caching.cache()
def get_background_brush():
    '''Get the default background brush.'''
    return wx.Brush(get_background_color())




### Color conversions: ########################################################
#                                                                             #
def wx_color_to_html_color(wx_color):
    '''Convert a wxPython color to an HTML color string.'''
    rgb = wx_color.GetRGB()
    (green_blue, red) = divmod(rgb, 256)
    (blue, green) = divmod(green_blue, 256)
    return '#%02x%02x%02x' % (red, green, blue)


def hls_to_wx_color(hls, alpha=255):
    '''Convert an HLS color to a wxPython color.'''
    return rgb_to_wx_color(colorsys.hls_to_rgb(*hls), alpha=alpha)


def wx_color_to_hls(wx_color):
    '''Convert a wxPython color to an HLS color.'''
    return colorsys.rgb_to_hls(wx_color.red, wx_color.blue, wx_color.green)


def rgb_to_wx_color(rgb, alpha=255):
    '''Convert an RGB color to a wxPython color.'''
    r, g, b = rgb
    return wx.Colour(r * 255, g * 255, b * 255, alpha)


def wx_color_to_rgb(wx_color):
    '''Convert a wxPython color to an RGB color.'''
    return (
        wx_color.red / 255,
        wx_color.green / 255,
        wx_color.blue / 255
    )


def wx_color_to_big_rgb(wx_color):
    '''Convert a wxPython color to a big (i.e. `int`) RGB color.'''
    return (
        wx_color.red,
        wx_color.green,
        wx_color.blue
    )
#                                                                             #
### Finished color conversions. ###############################################

### Color inversion: ##########################################################
#                                                                             #
def invert_rgb(rgb):
    red, green, blue = rgb
    return (
        1 - red,
        1 - green,
        1 - blue
    )


def invert_hls(hls):
    rgb = colorsys.hls_to_rgb(hls)
    inverted_rgb = inverted_rgb(rgb)
    return colorsys.rgb_to_hls(inverted_rgb)


def invert_wx_color(wx_color):
    rgb = wx_color_to_rgb(wx_color)
    inverted_rgb = invert_rgb(rgb)
    return rgb_to_wx_color(inverted_rgb)
#                                                                             #
### Finished color inversion. #################################################


def mix_wx_color(ratio, color1, color2):
    '''Mix two wxPython colors according to the given `ratio`.'''
    rgb = color_tools.mix_rgb(
        ratio,
        wx_color_to_rgb(color1),
        wx_color_to_rgb(color2)
    )
    return rgb_to_wx_color(rgb)
