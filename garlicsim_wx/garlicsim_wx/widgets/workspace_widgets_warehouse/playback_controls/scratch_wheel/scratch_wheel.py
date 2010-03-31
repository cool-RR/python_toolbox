# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
tododoc
'''


import wx
import math

import garlicsim
from garlicsim_wx.widgets import WorkspaceWidget

__all__ = ["ScratchWheel"]

class ScratchWheel(wx.Panel): # Gradient filling?
    
    def __init__(self, *args, **kwargs):
        
        if 'style' in kwargs:
            kwargs['style'] |= wx.SUNKEN_BORDER
        else:
            kwargs['style'] = wx.SUNKEN_BORDER
            
        wx.Panel.__init__(self, *args, **kwargs)
        
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.on_mouse_event)

        self.speed_function = lambda x: 20 * x ** 4
        
        self.current_angle = 0
        
        self.n_lines = 50
        
        self.line_width = 3

    def __calculate_lines(self):
        w = self.Size[0]
        d_angle = (2 * math.pi) / self.n_lines
        line_angles = (((self.current_angle + d_angle*i) % 2*math.pi) for i in
                       range(self.n_lines))
        visible_line_angles = (angle for angle in line_angles
                               if 0 <= angle <= math.pi)
        lines = (((w/2)*(1 + math.cos(angle)), math.sin(angle)*self.line_width)
                 for angle in visible_line_angles) # (pos, width) per line
        

    def on_paint(self, e=None):
        
        
        if (self.gui_project is None) or (self.gui_project.path is None):
            return
        
        (w, h) = self.GetSize()
        dc = wx.PaintDC(self)
        #dc.SetBrush(wx.Brush('#222222'))
        dc.FloodFill(1, 1, wx.Color(0x22, 0x22, 0x22))
        lines = self.__calculate_lines()
        rectangle_list = [(l_x - l_w/2., 0, l_w, h) for (l_x, l_w) in lines]
        dc.SetPen(wx.Pen('#AAAAAA'))
        dc.SetBrush(wx.Brush('#666666'))
        dc.DrawRectangleList(rectangle_list)
        
    

    def on_mouse_event(self, e):
        #print(dir(e))
        if e.RightDown():
            self.gui_project.stop_playing()

            reselect_node = False
            new_thing = e.GetPositionTuple()[0]
            if self.gui_project.active_node is None:
                reselect_node=True
            else:
                thing = self.screenify(self.gui_project.active_node.state.clock)
                if abs(thing - new_thing) >= 8:
                    reselect_node = True

            if reselect_node is True:
                
                new_node = self.gui_project.path.get_node_occupying_timepoint \
                         (self.unscreenify(new_thing))
                
                if new_node is not None:
                    self.gui_project.set_active_node(new_node, modify_path=False)

            if self.gui_project.active_node is not None:
                self.gui_project.frame.Refresh()
                self.PopupMenu(self.gui_project.get_node_menu(), e.GetPosition())



        if e.LeftDClick():
            self.gui_project.toggle_playing()
            
        if e.LeftDown():# or e.RightDown():
            thing = e.GetPositionTuple()[0]
            node = self.gui_project.path.get_node_occupying_timepoint \
                 (self.unscreenify(thing))

            self.was_playing_before_mouse_click = self.gui_project.is_playing
            if self.was_playing_before_mouse_click:
                self.gui_project.stop_playing()

            if node is not None:
                self.gui_project.set_active_node(node, modify_path=False)


        if e.LeftIsDown():
            thing = e.GetPositionTuple()[0]
            node = self.gui_project.path.get_node_occupying_timepoint \
                 (self.unscreenify(thing))
            if node is not None:
                self.gui_project.set_active_node(node, modify_path=False)
                
        if e.LeftUp():
            if self.was_playing_before_mouse_click:
                self.gui_project.start_playing()
                self.was_playing_before_mouse_click = False
                
        if e.Leaving():
            if self.was_playing_before_mouse_click:
                self.gui_project.start_playing()
                self.was_playing_before_mouse_click = False
                self.was_playing_before_mouse_click_but_then_paused_and_mouse_left = True
                
        if e.Entering():
            if self.was_playing_before_mouse_click_but_then_paused_and_mouse_left:
                self.gui_project.stop_playing()
                self.was_playing_before_mouse_click = True
                self.was_playing_before_mouse_click_but_then_paused_and_mouse_left = False


    def on_size(self, e):
        self.Refresh()
        if e is not None:
            e.Skip()
