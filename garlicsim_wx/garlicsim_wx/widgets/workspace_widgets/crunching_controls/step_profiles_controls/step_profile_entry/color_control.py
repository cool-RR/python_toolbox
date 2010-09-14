import colorsys

import wx

import garlicsim_wx


class ColorControl(wx.Window):
    def __init__(self, step_profile_entry, color=None):
        wx.Window.__init__(self, step_profile_entry, size=(25, 10),
                           style=wx.SIMPLE_BORDER)
        self.color = color or wx.Color(0, 0, 0)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        
            
    
    def on_paint(self, event):
        dc = wx.PaintDC(self)
        dc.SetBrush(wx.Brush(self.color))
        dc.DrawRectangle(0, 0, *self.GetSize())
        dc.Destroy()
        
        