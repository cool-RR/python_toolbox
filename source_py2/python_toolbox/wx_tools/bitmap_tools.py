# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines bitmap-related tools.'''

import pkg_resources
import wx


def color_replaced_bitmap(bitmap, old_rgb, new_rgb):
    '''Replace all appearances of `old_rgb` with `new_rgb` in `bitmap`.'''
    old_r, old_g, old_b = old_rgb
    new_r, new_g, new_b = new_rgb
    image = wx.ImageFromBitmap(bitmap)
    assert isinstance(image, wx.Image)
    image.Replace(old_r, old_g, old_b, new_r, new_g, new_b)
    return wx.BitmapFromImage(image)


def bitmap_from_pkg_resources(package_or_requirement, resource_name):
    '''
    Get a bitmap from a file using `pkg_resources`.
    
    Example:
    
        my_bitmap = bitmap_from_pkg_resources('whatever.images', 'image.jpg')
    
    '''
    return wx.BitmapFromImage(
        wx.ImageFromStream(
            pkg_resources.resource_stream(package_or_requirement,
                                          resource_name),
            wx.BITMAP_TYPE_ANY
        )
    )