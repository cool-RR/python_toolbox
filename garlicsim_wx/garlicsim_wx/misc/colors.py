# Copyright 2009-2011 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''Defines colors and color-related tools used in `garlicsim_wx`.'''

import colorsys

import wx


def make_wx_color(rgb):
    '''Convert an RGB float tuple (like `(0.1, 0.7, 0.3)`) to a `wx.Colour`.'''
    r, g, b = rgb
    return wx.Colour(255*r, 255*g, 255*b)

def hue_to_light_color(hue):
    '''Covert a float hue to a corresponding light `wx.Colour`.'''
    return make_wx_color(
        colorsys.hls_to_rgb(hue, 0.8, 1)
    )