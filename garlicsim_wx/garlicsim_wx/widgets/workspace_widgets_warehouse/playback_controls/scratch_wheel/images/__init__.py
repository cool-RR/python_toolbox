#todo
import wx
import pkg_resources

from . import images as __images_package
images_package = __images_package.__name__

N_FRAMES = 87

cached_images = []

def get_image(i):
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

cached_image_size = None

def get_image_size():
    if cached_image_size:
        return cached_image_size
    else:
        image = get_image(0)
        return image.GetSize()