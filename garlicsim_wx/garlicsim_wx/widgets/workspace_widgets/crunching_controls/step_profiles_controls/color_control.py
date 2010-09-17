import colorsys

import wx

import garlicsim_wx


class ColorControl(wx.Window):
    def __init__(self, step_profiles_list, color=None):
        wx.Window.__init__(self, step_profiles_list.GetMainWindow(),
                           size=(25, 10), style=wx.SIMPLE_BORDER)

        self.color = color or wx.Color(0, 0, 0)
        
        self._pen = wx.Pen(wx.Color(0, 0, 0), width=0, style=wx.TRANSPARENT)
        
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_mouse_left_down)
        
        
    
    def on_paint(self, event):
        dc = wx.PaintDC(self)
        dc.SetBrush(wx.Brush(self.color))
        dc.SetPen(self._pen)
        dc.DrawRectangle(0, 0, *self.GetSize())
        dc.Destroy()
        
    
    def on_mouse_left_down(self, event):
        1/0
        
        
    def set_color(self, color):
        if self.color != color:
            self.color = color
            self.Refresh()