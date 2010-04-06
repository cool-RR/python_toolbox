from __future__ import division
import wx
def draw_bitmap_to_dc_rotated(dc, bitmap, angle, point, useMask=useMask):
    """Rotate a bitmap and write it to the supplied device context."""
    img = bitmap.ConvertToImage()
    
    img_centre = wx.Point(
        img.GetWidth() / 2,
        img.GetHeight() / 2
    )
    
    img = img.Rotate(angle, img_centre, interpolating=True)
    
    new_point = (
        point[0] - img.GetWidth() / 2,
        point[1] - img.GetHeight() / 2
    )
    
    dc.DrawBitmapPoint(img.ConvertToBitmap(), new_point, useMask=useMask)