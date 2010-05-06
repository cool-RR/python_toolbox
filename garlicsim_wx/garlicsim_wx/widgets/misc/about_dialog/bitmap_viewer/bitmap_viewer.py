import wx

class BitmapViewer(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        #self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self._bitmap = wx.EmptyBitmap(1, 1)
        self.Bind(wx.EVT_PAINT, self.on_paint)
    
    def on_paint(self, event):
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self._bitmap, 0, 0)
        dc.Destroy()
        
    def set_bitmap(self, bitmap):
        self._bitmap = bitmap
        self.Refresh()