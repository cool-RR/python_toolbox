
import pkg_resources

import wx


_icon_bundle = None

def get_icon_bundle():
    
    global _icon_bundle
    
    if _icon_bundle:
        return _icon_bundle

    from . import images as __images_package
    images_package = __images_package.__name__

    ico_stream = pkg_resources.resource_stream(
        images_package,
        'garlicsim.ico'
    )
    
    _icon_bundle = wx.IconBundle()
    
    _icon_bundle.AddIconFromFile(ico_file, wx.BITMAP_TYPE_ICO)
    
    return _icon_bundle