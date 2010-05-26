# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''Images package.'''

import wx
import pkg_resources

from garlicsim.general_misc import caching

from . import images as __images_package
images_package = __images_package.__name__


N_FRAMES = 87
N_BLURRED_GEAR_FRAMES = 6

@caching.cache
def get_image_raw(i):
    '''Get image number `i` of the gear, when 0 <= i <= (N_FRAMES - 1).'''
    
    assert (0 <= i <= N_FRAMES - 1) and isinstance(i, int)
    
    file_name = 'gear%04.d.png' % i
    stream = pkg_resources.resource_stream(images_package, file_name)
    bitmap = wx.BitmapFromImage(
        wx.ImageFromStream(
            stream,
            wx.BITMAP_TYPE_ANY
        )
    )
    
    return bitmap
            

@caching.cache
def get_blur_image_raw(i):
    '''
    Get image number `i` of the blurred gear.

    The higher the `i`, the blurrier is the image.
    
    0 <= i <= (N_BLURRED_GEAR_FRAMES - 1)
    '''
    
    assert isinstance(i, int) and 0 <= i <= (N_BLURRED_GEAR_FRAMES - 1)
    
    file_name = 'blurred_gear_%d.png' % i
    stream = pkg_resources.resource_stream(images_package, file_name)
    bitmap = wx.BitmapFromImage(
        wx.ImageFromStream(
            stream,
            wx.BITMAP_TYPE_ANY
        )
    )

    return bitmap


@caching.cache
def get_blurred_gear_image(i, j):
    '''
    Get image number `i` of the gear, with motion blur number `j`.
    
    0 <= i <= (N_FRAMES - 1)
    0 <= j <= (N_BLURRED_GEAR_FRAMES - 1)
    '''
    image = get_image_raw(i)
    blur = get_blur_image_raw(j)
    bitmap = wx.EmptyBitmap(*get_image_size())
    dc = wx.MemoryDC(bitmap)
    dc.DrawBitmap(image, 0, 0)
    dc.DrawBitmap(blur, 0, 0, True)
    dc.Destroy()
    bitmap.image_raw = image
    bitmap.blur_raw = blur
    return bitmap
    

def get_blurred_gear_image_by_ratio(i, r):
    '''Get the image of the blurred gear by specifying a ratio from 0 to 1.'''
    assert 0 <= r <= 1
    return get_blurred_gear_image(
        i,
        int(round(r * (N_BLURRED_GEAR_FRAMES - 1)))
    )


@caching.cache
def get_image_size():
    '''Get the size of these images here.'''
    return get_image_raw(0).GetSize()
    
