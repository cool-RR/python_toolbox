from __future__ import division

import itertools
import math
import colorsys

import wx

from garlicsim.general_misc import caching
from garlicsim_wx.general_misc import wx_tools
from garlicsim_wx.general_misc import color_tools

BIG_LENGTH = 201
THICKNESS = 21
HALF_THICKNESS = THICKNESS / 2
AA_THICKNESS = 1.5
RADIUS = int((BIG_LENGTH / 2) - THICKNESS - 25)

two_pi = math.pi * 2


@caching.cache
def make_bitmap(lightness=1, saturation=1):
    bitmap = wx.EmptyBitmap(BIG_LENGTH, BIG_LENGTH)
    assert isinstance(bitmap, wx.Bitmap)
    dc = wx.MemoryDC(bitmap)
    
    dc.SetBrush(wx_tools.get_background_brush())
    dc.SetPen(wx.TRANSPARENT_PEN)
    dc.DrawRectangle(-5, -5, BIG_LENGTH + 10, BIG_LENGTH + 10)
    
    center_x = center_y = BIG_LENGTH // 2 
    wheel_start_radius = RADIUS - HALF_THICKNESS
    wheel_end_radius = RADIUS + HALF_THICKNESS
    background_color_rgb = wx_tools.wx_color_to_rgb(
        wx_tools.get_background_color()
    )
    
    for x, y in itertools.product(xrange(BIG_LENGTH), xrange(BIG_LENGTH)):
        distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
        
        if (wheel_start_radius - AA_THICKNESS) <= distance <= \
           (wheel_end_radius + AA_THICKNESS):
            
            angle = math.atan2((x - center_x), (y - center_y))
            hue = (angle % two_pi) / two_pi
            hls = (hue, lightness, saturation)
            raw_rgb = colorsys.hls_to_rgb(hue, lightness, saturation)
            
            if abs(distance - RADIUS) > HALF_THICKNESS:
                
                # This pixel requires some anti-aliasing.
                
                if distance < RADIUS:
                    aa_distance = wheel_start_radius - distance
                else: # distance > RADIUS
                    aa_distance = distance - wheel_end_radius
                
                aa_ratio = aa_distance / AA_THICKNESS
                
                final_rgb = color_tools.mix_rgb(
                    aa_ratio,
                    background_color_rgb,
                    raw_rgb
                )
            
            else:
                final_rgb = raw_rgb    
                
            color = wx_tools.rgb_to_wx_color(final_rgb)
            pen = wx.Pen(color)
            dc.SetPen(pen)
            
            dc.DrawPoint(x, y)
            #dc.DrawRectangle(x, y, 10, 10)
            
            
        
    
    #dc.SetPen(wx.Pen('red'))
    #dc.DrawLine(0, 0, 100, 100)
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
        
    