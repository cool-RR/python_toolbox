# Copyright 2009-2011 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the `CloseButton` class.

See its documentation for more details.
'''

import wx
import pkg_resources

from garlicsim.general_misc import caching

from . import images as __images_package
images_package = __images_package.__name__


@caching.cache()
def get_bitmap():
    '''Get the "X" bitmap used for the close button.'''
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
    '''Button for deleting a star-arg or star-kwarg.'''
    def __init__(self, parent):
        self.parent = parent
        wx.BitmapButton.__init__(self, parent, bitmap=get_bitmap())
                
            
        
