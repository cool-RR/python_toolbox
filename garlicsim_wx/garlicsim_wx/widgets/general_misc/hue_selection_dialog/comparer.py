# Copyright 2009-2011 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the `Comparer` class.

See its documentation for more details.
'''

import wx

from garlicsim_wx.general_misc import wx_tools


class Comparer(wx.Panel):
    '''Shows the new hue compared to the old hue before dialog was started.'''
    def __init__(self, hue_selection_dialog):
        style = wx.SIMPLE_BORDER if wx.Platform == '__WXGTK__' else \
                wx.SUNKEN_BORDER
        wx.Panel.__init__(self, parent=hue_selection_dialog, size=(75, 90),
                          style=style)
        self.SetDoubleBuffered(True)
        self.hue_selection_dialog = hue_selection_dialog
        self.hue = hue_selection_dialog.hue
        self.old_hls = hue_selection_dialog.old_hls
        self.old_hue = hue_selection_dialog.old_hue
        self.old_color = wx_tools.hls_to_wx_color(self.old_hls)
        self.old_brush = wx.Brush(self.old_color)
        self._pen = wx.Pen(wx.Colour(0, 0, 0), width=0, style=wx.TRANSPARENT)
        self._calculate()
        
        self.SetCursor(wx.StockCursor(wx.CURSOR_BULLSEYE))
        
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_mouse_left_down)
        
        
    def _calculate(self):
        '''Create a brush for showing the new hue.'''
        self.color = wx_tools.hls_to_wx_color(
            (self.hue,
             self.hue_selection_dialog.lightness,
             self.hue_selection_dialog.saturation)
        )
        self.brush = wx.Brush(self.color)
        
        
    def update(self):
        '''If hue changed, show new hue.'''
        if self.hue != self.hue_selection_dialog.hue:
            self.hue = self.hue_selection_dialog.hue
            self._calculate()
            self.Refresh()

            
    def on_paint(self, event):
        w, h = self.GetClientSize()
        dc = wx.PaintDC(self)

        dc.SetPen(self._pen)
        
        dc.SetBrush(self.brush)
        dc.DrawRectangle(0, 0, w, (h // 2))
        
        dc.SetBrush(self.old_brush)
        dc.DrawRectangle(0, (h // 2), w, (h // 2) + 1)
        
                
    
    def on_mouse_left_down(self, event):
        x, y = event.GetPosition()
        w, h = self.GetClientSize()
        if y >= h // 2:
            self.hue_selection_dialog.setter(self.old_hue)