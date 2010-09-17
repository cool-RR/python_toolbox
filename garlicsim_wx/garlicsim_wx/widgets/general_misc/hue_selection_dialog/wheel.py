import wx

from garlicsim.general_misc import caching
from garlicsim_wx.general_misc import wx_tools

WIDTH, HEIGHT = 300, 300

@caching.cache
def make_bitmap(lightness=1, saturation=1):
    bitmap = wx.EmptyBitmap(300, 300)
    dc = wx.MemoryDC(bitmap)
    dc.SetBrush(wx_tools.get_background_brush())
    dc.Dra
    
    dc.SetPen(wx.Pen('red'))
    dc.DrawLine(0, 0, 100, 100)
    dc.Destroy()
    return bitmap

class Wheel(wx.Panel):
    def __init__(self, hue_selection_dialog):
        wx.Panel.__init__(self, parent=hue_selection_dialog, size=(300, 300))
        self.hue_selection_dialog = hue_selection_dialog
        self.lightness = hue_selection_dialog.lightness # tododoc: needed?
        self.saturation = hue_selection_dialog.saturation # tododoc: needed?
        self.bitmap = make_bitmap(hue_selection_dialog.lightness,
                                  hue_selection_dialog.saturation)
        
        self.Bind(wx.EVT_PAINT, self.on_paint)
        
    
    def on_paint(self, event):
        dc = wx.PaintDC(self)
                    
        bw, bh = self.GetWindowBorderSize()
        ox, oy = ((4 - bw) / 2 , (4 - bh) / 2) #tododoc: doc
        
        dc.DrawBitmap(self.bitmap, ox, oy)
        
        dc.Destroy()
        
    