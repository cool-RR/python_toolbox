#tododoc
#todo: possibly change terminology from image to bitmap
import wx
import pkg_resources

from . import images as __images_package
images_package = __images_package.__name__

N_FRAMES = 87

cached_images = []
cached_motion_blur_image = None

def get_image(i):
    
    global N_FRAMES, cached_images
    
    assert isinstance(i, int) and 0 <= i <= (N_FRAMES - 1)
    if not cached_images:
        for j in range(N_FRAMES):
            file_name = 'gear%04.d.png' % j
            full_path = pkg_resources.resource_filename(images_package,
                                                        file_name)
            bitmap = wx.Bitmap(full_path, wx.BITMAP_TYPE_ANY)
            cached_images.append(bitmap)
    
    assert len(cached_images) == N_FRAMES
    
    return cached_images[i]

def get_motion_blur_image():
    
    global cached_motion_blur_image
    
    if cached_motion_blur_image is None:
        full_path = pkg_resources.resource_filename(images_package,
                                                    'motion_blur.png')
        bitmap = wx.Bitmap(full_path, wx.BITMAP_TYPE_ANY)
        cached_motion_blur_image = bitmap
    
    return cached_motion_blur_image


cached_image_size = None

def get_image_size():
    global cached_image_size
    
    if cached_image_size is None:
        image = get_image(0)
        cached_image_size = image.GetSize()
    
    return cached_image_size
    
