# Copyright 2009-2011 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''Defines an icon bundle for GarlicSim.'''

import pkg_resources

import wx

from garlicsim.general_misc import caching


@caching.cache()
def get_icon_bundle():
    '''Get GarlicSim's icon bundle.'''

    from . import images as __images_package
    images_package = __images_package.__name__

    icons = []
    for size in [16, 24, 32, 48, 96, 128, 256]:
        file_name = 'icon%s.png' % str(size)
        stream = pkg_resources.resource_stream(
            images_package,
            file_name
        )
        icon = wx.IconFromBitmap(
            wx.BitmapFromImage(
                wx.ImageFromStream(
                    stream,
                    wx.BITMAP_TYPE_PNG
                )
            )
        )
        icons.append(icon)
        
        # todo: should probably be loading the bitmaps from the .ico file, to
        # save on storing all those PNGs.
                    
    icon_bundle = wx.IconBundle()
    
    for icon in icons:
        icon_bundle.AddIcon(icon)
    
    return icon_bundle