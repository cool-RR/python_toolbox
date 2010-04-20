
import math

import wx
import garlicsim_wx


class StateViewer(wx.Window, garlicsim_wx.widgets.WorkspaceWidget):
    '''Widget for showing a state onscreen.'''
    def __init__(self, frame):
        wx.Window.__init__(self, frame)
        garlicsim_wx.widgets.WorkspaceWidget.__init__(self, frame)
        
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        
        self.left = None
        self.right = None
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.radius = 60
        
        self.gui_project.active_node_changed_emitter.add_output(
            lambda: self.load_state(self.gui_project.active_node.state)
        )
        
    def on_paint(self, event):
        '''Paint event handler.'''
        event.Skip()
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
        