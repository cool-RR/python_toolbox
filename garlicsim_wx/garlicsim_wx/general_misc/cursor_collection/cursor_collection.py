# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''A collection of cursors.'''

# todo: change to use generic caching decorator

import pkg_resources
import wx

from . import images as __images_package
images_package = __images_package.__name__

cached_cursors = {}

def get_open_grab():
    '''Get the "open grab" cursor.'''
    name = 'open_grab'
    file_name = 'open_grab.png'
    hotspot = (8, 8)
    if name in cached_cursors:
        return cached_cursors[name]
    stream = pkg_resources.resource_stream(images_package,
                                           file_name)
    image = wx.ImageFromStream(stream, wx.BITMAP_TYPE_ANY)

    if hotspot is not None:
        image.SetOptionInt(wx.IMAGE_OPTION_CUR_HOTSPOT_X, hotspot[0])
        image.SetOptionInt(wx.IMAGE_OPTION_CUR_HOTSPOT_Y, hotspot[1])
        
    cursor = wx.CursorFromImage(image)
    cached_cursors[name] = cursor
    return cursor


def get_closed_grab():
    '''Get the "closed grab" cursor.'''
    name = 'closed_grab'
    file_name = 'closed_grab.png'
    hotspot = (8, 8)
    if name in cached_cursors:
        return cached_cursors[name]
    stream = pkg_resources.resource_stream(images_package,
                                           file_name)
    image = wx.ImageFromStream(stream, wx.BITMAP_TYPE_ANY)

    if hotspot is not None:
        image.SetOptionInt(wx.IMAGE_OPTION_CUR_HOTSPOT_X, hotspot[0])
        image.SetOptionInt(wx.IMAGE_OPTION_CUR_HOTSPOT_Y, hotspot[1])
        
    cursor = wx.CursorFromImage(image)
    cached_cursors[name] = cursor
    return cursor
