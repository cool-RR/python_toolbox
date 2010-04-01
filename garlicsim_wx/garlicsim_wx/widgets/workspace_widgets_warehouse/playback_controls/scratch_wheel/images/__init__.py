
import wx

from . import images as __images_package
images_package = __images_package.__name__

cached_images = []

def get_image(i):
    assert isinstance(i, int) and 0 <= i <=