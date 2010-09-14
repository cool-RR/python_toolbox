import colorsys

import wx

import garlicsim_wx


class XColorControl(wx.Window):
    def __init__(self, step_profiles_list, color=None):
        wx.Window.__init__(self, step_profiles_list.GetMainWindow(),
                           size=(25, 10), style=wx.SIMPLE_BORDER)
        self.color = color or wx.Color(0, 0, 0)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        
    
    def on_paint(self, event):
        dc = wx.PaintDC(self)
        dc.SetBrush(wx.Brush(self.color))
        dc.DrawRectangle(0, 0, *self.GetSize())
        dc.Destroy()
        
    
    def set_color(self, color):
        if self.color != color:
            self.color = color
            self.Refresh()