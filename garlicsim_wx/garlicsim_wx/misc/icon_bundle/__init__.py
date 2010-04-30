
import pkg_resources

import wx



_icon_bundle = None

def get_icon_bundle():
    
    global _icon_bundle
    
    if _icon_bundle:
        return _icon_bundle

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
                    
    
    _icon_bundle = wx.IconBundle()
    
    for icon in icons:
        _icon_bundle.AddIcon(icon)
    
    return _icon_bundle