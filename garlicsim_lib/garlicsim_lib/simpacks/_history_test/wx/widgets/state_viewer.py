# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `StateViewer` class.

See its documentation for more information.
'''

import math
import wx

from garlicsim_wx.general_misc import wx_tools
from garlicsim_wx.widgets.general_misc.cute_window import CuteWindow

import garlicsim_wx


class StateViewer(garlicsim_wx.widgets.WorkspaceWidget, CuteWindow):
    '''Widget for showing a state onscreen.'''
    
    def __init__(self, frame):
        CuteWindow.__init__(self, frame, style=wx.SUNKEN_BORDER)
        garlicsim_wx.widgets.WorkspaceWidget.__init__(self, frame)
        
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        
        self.left = None
        self.right = None
        self.radius = 60
        
        self.gui_project.active_node_changed_or_modified_emitter.add_output(
            lambda: self.load_state(self.gui_project.get_active_state())
        )
        
        self.bind_event_handlers(StateViewer)
        
        
    def _on_paint(self, event):
        event.Skip()
        dc = wx.BufferedPaintDC(self)
                
        dc.SetBackground(wx_tools.colors.get_background_brush())
        dc.Clear()
        
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
        if state is None:
            return
        self.left, self.right = state.left, state.right
        self.Refresh()
        