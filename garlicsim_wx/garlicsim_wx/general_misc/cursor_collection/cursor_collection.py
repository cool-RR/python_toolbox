#tododoc

import pkg_resources
import wx

from . import images as __images_package
images_package = __images_package.__name__



cursors_info = {
    'open_grab': ('open_grab.png', (8, 8)),
    'closed_grab': ('closed_grab.png', (8, 8)),
}

cached_cursors = {}

for (name, (file_name, hotspot)) in cursors_info.iteritems():
    
    def get_cursor():
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
        
    locals()['get_' + name] = get_cursor
