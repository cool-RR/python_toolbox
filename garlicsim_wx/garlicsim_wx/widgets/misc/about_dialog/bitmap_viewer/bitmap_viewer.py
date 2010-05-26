# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the BitmapViewer class.

See its documentation for more info.
'''

import wx

class BitmapViewer(wx.Panel):
    '''Widget for viewing a bitmap. Similar to StaticBitmap.'''
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        #self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self._bitmap = wx.EmptyBitmap(1, 1)
        self.Bind(wx.EVT_PAINT, self.on_paint)
    
    def on_paint(self, event):
        '''EVT_PAINT handler.'''
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self._bitmap, 0, 0)
        dc.Destroy()
        
    def set_bitmap(self, bitmap):
        '''Set the bitmap that the viewer will display.'''
        self._bitmap = bitmap
        self.Refresh()