# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''A collection of cursors.'''

import pkg_resources
import wx

from python_toolbox import caching


from . import images as __images_package
images_package = __images_package.__name__


@caching.cache()
def get_open_grab():
    '''Get the "open grab" cursor.'''
    file_name = 'open_grab.png'
    hotspot = (8, 8)
    stream = pkg_resources.resource_stream(images_package,
                                           file_name)
    image = wx.ImageFromStream(stream, wx.BITMAP_TYPE_ANY)

    if hotspot is not None:
        image.SetOptionInt(wx.IMAGE_OPTION_CUR_HOTSPOT_X, hotspot[0])
        image.SetOptionInt(wx.IMAGE_OPTION_CUR_HOTSPOT_Y, hotspot[1])
        
    cursor = wx.CursorFromImage(image)
    return cursor


@caching.cache()
def get_closed_grab():
    '''Get the "closed grab" cursor.'''
    file_name = 'closed_grab.png'
    hotspot = (8, 8)
    stream = pkg_resources.resource_stream(images_package,
                                           file_name)
    image = wx.ImageFromStream(stream, wx.BITMAP_TYPE_ANY)

    if hotspot is not None:
        image.SetOptionInt(wx.IMAGE_OPTION_CUR_HOTSPOT_X, hotspot[0])
        image.SetOptionInt(wx.IMAGE_OPTION_CUR_HOTSPOT_Y, hotspot[1])
        
    cursor = wx.CursorFromImage(image)
    return cursor
