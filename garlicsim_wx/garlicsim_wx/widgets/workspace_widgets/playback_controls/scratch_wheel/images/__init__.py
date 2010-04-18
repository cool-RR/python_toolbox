#tododoc
#todo: possibly change terminology from image to bitmap
import wx
import pkg_resources

from . import images as __images_package
images_package = __images_package.__name__

N_FRAMES = 87
N_BLURRED_GEAR_FRAMES = 6

cached_images = []
cached_blurred_gear_images = []

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

def get_blurred_gear_image(i):
    
    global N_FRAMES, cached_blurred_gear_images
    
    assert isinstance(i, int) and 0 <= i <= (N_BLURRED_GEAR_FRAMES - 1)
    if not cached_blurred_gear_images:
        for j in range(N_BLURRED_GEAR_FRAMES):
            file_name = 'blurred_gear_%d.png' % j
            full_path = pkg_resources.resource_filename(images_package,
                                                        file_name)
            bitmap = wx.Bitmap(full_path, wx.BITMAP_TYPE_ANY)
            cached_blurred_gear_images.append(bitmap)
    
    assert len(cached_blurred_gear_images) == N_BLURRED_GEAR_FRAMES
    
    return cached_blurred_gear_images[i]

def get_blurred_gear_image_by_ratio(r):
    assert 0 <= r <= 1
    return get_blurred_gear_image(
        int(round(r * (N_BLURRED_GEAR_FRAMES - 1)))
    )

cached_image_size = None

def get_image_size():
    global cached_image_size
    
    if cached_image_size is None:
        image = get_image(0)
        cached_image_size = image.GetSize()
    
    return cached_image_size
    
