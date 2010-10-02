from __future__ import division

import wx


class ActiveStepProfileIndicator(wx.Window):
    def __init__(self, step_profile_item_panel, step_profile):
        self.step_profile_item_panel = step_profile_item_panel
        self.active = False
        wx.Window.__init__(self, step_profile_item_panel, size=(10, -1))
        self.SetBackgroundColour(step_profile_item_panel.GetBackgroundColour())
        self.Bind(wx.EVT_PAINT, self.on_paint)
        
    
    def set_active(self):
        if not self.active:
            self.active = True
            self.Refresh()

            
    def set_inactive(self):
        if  self.active:
            self.active = False
            self.Refresh()
            
        
    def on_paint(self, event):
        dc = wx.BufferedPaintDC(self)
        #dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        if self.active:
            gc = wx.GraphicsContext.Create(dc)
            assert isinstance(gc, wx.GraphicsContext)
            w, h = self.GetClientSize()
            path = gc.CreatePath()
            assert isinstance(path, wx.GraphicsPath)
            path.MoveToPoint((1/4) * w, (1/6) * h)
            path.AddLineToPoint((1/4) * w, (5/6) * h)
            path.AddLineToPoint((5/6) * w, (1/2) * h)
            #path.CloseSubpath()
            gc.SetPen(wx.Pen(wx.Color(255, 0, 0)))#gc.SetPen(wx.TRANSPARENT_PEN)
            gc.SetBrush(wx.Brush(wx.Color(0, 0, 0)))
            #gc.StrokeLine(0, 0, 3, 3)
            gc.FillPath(path)
            gc.Destroy()
        
        
        dc.Destroy()