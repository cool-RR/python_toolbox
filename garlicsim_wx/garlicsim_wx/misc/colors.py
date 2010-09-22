import colorsys

import wx


def make_wx_color(rgb):
    r, g, b = rgb
    return wx.Color(255*r, 255*g, 255*b)

def hue_to_light_color(hue):
    return make_wx_color(
        colorsys.hls_to_rgb(hue, 0.8, 1)
    )