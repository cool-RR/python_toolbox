#tododoc

import pkg_resources
import wx

from . import images as __images_package
images_package = __images_package.__name__

cached_cursors = {}


def get_open_grab():
    name = 'open_grab'
    file_name = 'open_grab.png'
    hotspot = (8, 8)
    if name in cached_cursors:
        return cached_cursors[name]
    full_path = pkg_resources.resource_filename(images_package,
                                                file_name)
    image = wx.Image(full_path, wx.BITMAP_TYPE_ANY)

    if hotspot is not None:
        image.SetOptionInt(wx.IMAGE_OPTION_CUR_HOTSPOT_X, hotspot[0])
        image.SetOptionInt(wx.IMAGE_OPTION_CUR_HOTSPOT_Y, hotspot[1])
        
    cursor = wx.CursorFromImage(image)
    cached_cursors[name] = cursor
    return cursor


def get_closed_grab():
    name = 'closed_grab'
    file_name = 'closed_grab.png'
    hotspot = (8, 8)
    if name in cached_cursors:
        return cached_cursors[name]
    full_path = pkg_resources.resource_filename(images_package,
                                                file_name)
    image = wx.Image(full_path, wx.BITMAP_TYPE_ANY)

    if hotspot is not None:
        image.SetOptionInt(wx.IMAGE_OPTION_CUR_HOTSPOT_X, hotspot[0])
        image.SetOptionInt(wx.IMAGE_OPTION_CUR_HOTSPOT_Y, hotspot[1])
        
    cursor = wx.CursorFromImage(image)
    cached_cursors[name] = cursor
    return cursor
