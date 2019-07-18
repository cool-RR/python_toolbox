# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines functions for getting generic bitmaps, sometimes from the OS.'''

import wx

from python_toolbox import caching


is_mac = (wx.Platform == '__WXMAC__')
is_gtk = (wx.Platform == '__WXGTK__')
is_win = (wx.Platform == '__WXMSW__')


@caching.cache()
def _get_icon_bitmap_from_shell32_dll(index_number, size):
    assert isinstance(index_number, int)
    assert is_win

    import win32api

    width, height = size
    shell32_dll = win32api.GetModuleFileName(
        win32api.GetModuleHandle('shell32.dll')
    )
    return wx.BitmapFromIcon(
        wx.Icon(
            '%s;%s' % (shell32_dll, index_number),
            wx.BITMAP_TYPE_ICO,
            desiredWidth=width,
            desiredHeight=height
        )
    )

@caching.cache()
def get_closed_folder_bitmap(size=(16, 16)):
    if is_win:
        return _get_icon_bitmap_from_shell32_dll(3, size=size)
    else:
        return wx.ArtProvider_GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, size)

@caching.cache()
def get_open_folder_bitmap(size=(16, 16)):
    if is_win:
        return _get_icon_bitmap_from_shell32_dll(4, size=size)
    else:
        return wx.ArtProvider_GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, size)