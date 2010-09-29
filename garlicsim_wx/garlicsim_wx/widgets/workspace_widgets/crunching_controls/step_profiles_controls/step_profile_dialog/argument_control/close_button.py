import wx
import pkg_resources

from garlicsim.general_misc import caching
from garlicsim_wx.general_misc import wx_tools

from . import images as __images_package
images_package = __images_package.__name__


@caching.cache()
def get_bitmap():

    stream = pkg_resources.resource_stream(
        images_package,
        'close.png'
    )
    
    return wx.BitmapFromImage(
        wx.ImageFromStream(
            stream,
            wx.BITMAP_TYPE_ANY
        )
    )


class CloseButton(wx.BitmapButton):
    def __init__(self, parent):
        self.parent = parent
        
        wx.BitmapButton.__init__(self, parent, bitmap=get_bitmap())
                
            
        
