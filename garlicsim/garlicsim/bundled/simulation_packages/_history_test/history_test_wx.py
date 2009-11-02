# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Definitions for garlicsim_wx.'''

import wx
import math

def initialize(gui_project):
    '''Initialize the gui.'''
    gui_project.state_shower = StateShower(gui_project.state_showing_window)
    sizer=wx.BoxSizer(wx.VERTICAL)
    sizer.Add(gui_project.state_shower, 1, wx.EXPAND)
    gui_project.state_showing_window.SetSizer(sizer)


def show_state(gui_project, state):
    '''Show the state onscreen.'''
    gui_project.state_shower.load_state(state)


class StateShower(wx.Window):
    '''Widget for showing a state onscreen.'''
    def __init__(self, *args, **kwargs):
        wx.Window.__init__(self, *args, **kwargs)
        self.left = None
        self.right = None
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.radius = 60
        
    def on_paint(self, event=None):
        '''Paint event handler.'''
        dc = wx.PaintDC(self)
        dc.SetBrush(wx.Brush("white", wx.TRANSPARENT))
        for [side, pos] in [[self.left, (100, 100)], [self.right, (300, 100)]]:
            
            dc.SetPen(wx.Pen("black", 2))
            dc.DrawCirclePoint(pos, self.radius)
            
            if side is not None:
                point = (pos[0] + math.cos(side) * self.radius,
                         pos[1] + math.sin(side) * self.radius)
                dc.SetPen(wx.Pen("red", 20))
                dc.DrawLinePoint(point, point)
    
    def load_state(self, state):
        '''Load a state and show it onscreen.'''
        self.left, self.right = state.left, state.right
        self.Refresh()
        