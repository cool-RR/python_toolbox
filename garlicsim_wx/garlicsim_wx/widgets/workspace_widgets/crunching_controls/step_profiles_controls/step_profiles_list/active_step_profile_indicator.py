# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `ActiveStepProfileIndicator` class.

See its documentation for more details.
'''

from __future__ import division

import wx


class ActiveStepProfileIndicator(wx.Window):
    '''
    Widget for indicating which step profile is active.
    
    This widget appears next to *every* step profile in the list; but only for
    the active step profile it shows a little black triangle, while for the
    others it shows nothing.
    '''
    def __init__(self, step_profile_item_panel, step_profile, size=(10, 15)):
        self.step_profile_item_panel = step_profile_item_panel
        self.active = False
        wx.Window.__init__(self, step_profile_item_panel, size=size)
        self.SetMinSize(size)
        self.SetBackgroundColour(step_profile_item_panel.GetBackgroundColour())
        self.Bind(wx.EVT_PAINT, self._on_paint)
        
    
    def set_active(self):
        '''Set this `ActiveStepProfileIndicator` to show a marker.'''
        if not self.active:
            self.active = True
            self.Refresh()

            
    def set_inactive(self):
        '''Set this `ActiveStepProfileIndicator` to not show a marker.'''
        if self.active:
            self.active = False
            self.Refresh()
            
        
    def _on_paint(self, event):
        dc = wx.BufferedPaintDC(self)
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
            gc.SetPen(wx.Pen(wx.Colour(255, 0, 0)))
            gc.SetBrush(wx.Brush(wx.Colour(0, 0, 0)))
            gc.FillPath(path)
            gc.Destroy()
        
        
        dc.Destroy()