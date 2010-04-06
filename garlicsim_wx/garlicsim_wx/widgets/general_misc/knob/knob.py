

import wx

class Knob(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        
        wx.Panel.__init__(self, parent, *args, size=(30, 30), **kwargs)