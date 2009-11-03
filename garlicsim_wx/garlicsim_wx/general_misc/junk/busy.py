import wx
import random

NUMBER_OF_LINES = 10000 # Increase this if you were blessed with a very strong computer

def random_point():
    return (random.random()*500, random.random()*500)

class Frame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        self.SetDoubleBuffered(True)
        window = Window(self)
        self.Show()
        
class Window(wx.Window):
    def __init__(self, *args, **kwargs):
        wx.Window.__init__(self, *args, **kwargs)
        
        self.Bind(wx.EVT_PAINT, self.on_paint)
        
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer)
        self.timer.Start(5)
        
    def on_timer(self, event=None):
        self.Refresh()
        
    def on_paint(self, event=None):
        dc = wx.PaintDC(self)
        for i in xrange(NUMBER_OF_LINES):
            dc.DrawLinePoint(random_point(), random_point())


if __name__ == "__main__":
    app = wx.PySimpleApp()
    my_frame = Frame(None)
    
    app.MainLoop()