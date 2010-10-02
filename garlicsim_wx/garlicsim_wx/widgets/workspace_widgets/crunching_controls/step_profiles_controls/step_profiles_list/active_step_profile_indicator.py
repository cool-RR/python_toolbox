import wx


class ActiveStepProfileIndicator(wx.Window):
    def __init__(self, step_profile_item_panel, step_profile):
        self.step_profile_item_panel = step_profile_item_panel
        self.active = False
        wx.Window.__init__(self, step_profile_item_panel)
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
        dc.SetBrush(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        if self.active:
            gc = wx.GraphicsContext.Create(dc)
            assert isinstance(gc, wx.GraphicsContext)
            w, h = self.GetClientSize()
            path = gc.CreatePath()
            assert isinstance(path, wx.GraphicsPath)
            path.MoveToPoint((1/4) * w, (1/3) * h)
            path.AddLineToPoint((1/4) * w, (2/3) * h)
            path.AddLineToPoint((1/4) * w, (1/3) * h)
            gc.SetPen(wx.TRANSPARENT_PEN)
            gc.SetBrush(wx.Brush(wx.Color(0, 0, 0)))
            gc.DrawPath(path)
            gc.Destroy()
        
        
        dc.Destroy()