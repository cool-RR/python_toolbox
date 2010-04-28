
import pkg_resources

import wx


_icon_bundle = None

def get_icon_bundle():
    
    global _icon_bundle
    
    if _icon_bundle:
        return _icon_bundle

    from . import images as __images_package
    images_package = __images_package.__name__

    ico_file = pkg_resources.resource_filename(
        images_package,
        'garlicsim.ico'
    )
    
    icns_file = pkg_resources.resource_filename(
        images_package,
        'garlicsim.icns'
    )
    
    _icon_bundle = wx.IconBundle()
    
    _icon_bundle.AddIconFromFile(ico_file, wx.BITMAP_TYPE_ANY)
    #_icon_bundle.AddIconFromFile(icns_file, wx.BITMAP_TYPE_ANY)
    
    return _icon_bundle