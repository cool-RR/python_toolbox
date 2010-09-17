from __future__ import division

import itertools
import math
import colorsys

import wx

from garlicsim.general_misc import caching
from garlicsim_wx.general_misc import wx_tools
from garlicsim_wx.general_misc import color_tools

BIG_LENGTH = 301
THICKNESS = 21
AA_THICKNESS = 2
RADIUS = int((LENGTH / 2) - THICKNESS - 25)


@caching.cache
def make_bitmap(lightness=1, saturation=1):
    bitmap = wx.EmptyBitmap(BIG_LENGTH, BIG_LENGTH)
    assert isinstance(bitmap, wx.Bitmap)
    dc = wx.MemoryDC(bitmap)
    
    dc.SetBrush(wx_tools.get_background_brush())
    dc.SetPen(wx.TRANSPARENT_PEN)
    dc.DrawRectangle(-5, 5, BIG_LENGTH + 10, BIG_LENGTH + 10)
    
    center_x = center_y = BIG_LENGTH // 2 
    wheel_start_radius = RADIUS - THICKNESS / 2
    wheel_end_radius = RADIUS + THICKNESS / 2
    background_color = wx_tools.get_background_color()
    
    for x, y in itertools.product(xrange(BIG_LENGTH), xrange(BIG_LENGTH)):
        distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
        
        if (wheel_start_radius - AA_THICKNESS) <= distance <= \
           (wheel_end_radius + AA_THICKNESS):
            
            hue = math.asin((x - center_x)/(y - center_y))
            raw_rgb = colorsys.hls_to_rgb(hue, lightness, saturation)
            
            if abs(distance - RADIUS) > THICKNESS:
                
                # This pixel requires some anti-aliasing.
                
                if distance < RADIUS:
                    aa_distance = wheel_start_radius - distance
                else: # distance > RADIUS
                    aa_distance = distance - wheel_end_radius
                
                aa_ratio = aa_distance / AA_THICKNESS
                
                final_rgb = \
                    color_tools.mix_rgb(aa_ratio, background_color, raw_rgb)
                    
            
        
    
    dc.SetPen(wx.Pen('red'))
    dc.DrawLine(0, 0, 100, 100)
    dc.Destroy()
    return bitmap


class Wheel(wx.Panel):
    def __init__(self, hue_selection_dialog):
        wx.Panel.__init__(self, parent=hue_selection_dialog, size=(BIG_LENGTH, BIG_LENGTH))
        self.hue_selection_dialog = hue_selection_dialog
        self.lightness = hue_selection_dialog.lightness # tododoc: needed?
        self.saturation = hue_selection_dialog.saturation # tododoc: needed?
        self.bitmap = make_bitmap(hue_selection_dialog.lightness,
                                  hue_selection_dialog.saturation)
        
        self.Bind(wx.EVT_PAINT, self.on_paint)
        
    
    def on_paint(self, event):
        dc = wx.PaintDC(self)
                    
        bw, bh = self.GetWindowBorderSize()
        ox, oy = ((4 - bw) / 2 , (4 - bh) / 2) #tododoc: test and doc
        
        dc.DrawBitmap(self.bitmap, ox, oy)
        
        dc.Destroy()
        
    