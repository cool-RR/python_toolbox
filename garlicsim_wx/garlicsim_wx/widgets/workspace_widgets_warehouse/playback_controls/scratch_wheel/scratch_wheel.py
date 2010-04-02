# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
tododoc
'''

from __future__ import division

import wx
import math

import garlicsim, garlicsim_wx
from garlicsim_wx.widgets import WorkspaceWidget
from garlicsim_wx.general_misc import cursor_collection

import images

__all__ = ["ScratchWheel"]

def pos_to_angle(pos):
    return -math.acos(-1 + 2*pos)


def expanded_pos_to_angle(pos):
    #if 0 <= pos <= 1:
    #    return -math.acos(-1 + 2*pos)
    #else:
    pos = (pos * 0.8) + 0.1
    return -math.pi * (1 - pos)

#def angle_to_pos(angle):
#    return (1 + math.cos(-angle)) / 2


class ScratchWheel(wx.Panel): # Gradient filling?
    #This shit needs to get redrawed often enough to see the wheel move when playing
    def __init__(self, parent, gui_project, *args, **kwargs):
        
        if 'style' in kwargs:
            kwargs['style'] |= wx.SUNKEN_BORDER
        else:
            kwargs['style'] = wx.SUNKEN_BORDER
            
        wx.Panel.__init__(self, parent, *args, **kwargs)
        
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.on_mouse_event)
        
        self.Unbind(wx.EVT_ERASE_BACKGROUND) # Good or bad?

        self.SetCursor(cursor_collection.get_open_grab())
        
        self.gui_project = gui_project
        
        assert isinstance(self.gui_project, garlicsim_wx.GuiProject)
        
        self.speed_function = lambda x: 20 * x ** 4
        
        self.n_lines = 15
        
        self.line_width = 20

        self.frame_number_that_should_be_drawn = None
        
        self.current_frame_number = -1
        # Set to -1 to make sure first drawing won't fuck up
        
        self.image_size = images.get_image_size()
        
        self.clock_factor = 0.05 # todo: maybe rename
        
        self.being_grabbed = False
        
        self.grabbed_angle = None
        self.grabbed_pseudoclock = None
        self.angle_while_grabbing = None
        self.d_angle_while_grabbing = None
        self.desired_clock_while_grabbing = None
        
        self.was_playing_before_drag = None
        
        self.__calculate_frame_number()

        
    def get_current_angle(self):
        return (self.__get_current_pseudoclock() * self.clock_factor) % \
               (2*math.pi)
    
    def __get_current_pseudoclock(self): 
        gui_project = self.gui_project
        
        if gui_project is None or gui_project.active_node is None:
            return 0
        
        active_node = self.gui_project.active_node
        
        if self.being_grabbed is True:
            
            if active_node.parent is None or len(active_node.children) == 0:
                return active_node.state.clock
            else:
                return self.desired_clock_while_grabbing
        
        elif gui_project.is_playing:
            return gui_project.simulation_time_krap or \
                   active_node.state.clock
        else:
            return active_node.state.clock
                    
    def __calculate_frame_number(self):
        angle = self.get_current_angle()
        frame_number = int(
            ((angle % ((2/3) * math.pi)) / (2 * math.pi)) * 3 * images.N_FRAMES
        )
        if frame_number == images.N_FRAMES:
            frame_number =- 1
        
        self.frame_number_that_should_be_drawn = frame_number
    
    def __redraw_if_wheel_should_rotate(self):
        self.__calculate_frame_number()
        if self.frame_number_that_should_be_drawn != self.current_frame_number:
            self.Refresh()
        
    def on_paint(self, e=None):
        
        
        if self.gui_project is None:
            return
        
        (w, h) = self.GetClientRect()[2:4]
        
        (iw, ih) = self.image_size

        (ix, iy) = ((w-iw)/2, (h-ih)/2)
        
        
        bitmap = images.get_image(self.frame_number_that_should_be_drawn)
        dc = wx.PaintDC(self)
        dc.DrawBitmap(bitmap, ix, iy)
        self.current_frame_number = self.frame_number_that_should_be_drawn
            
        
    def on_mouse_event(self, e):
        #todo: possibly do momentum, like in old shockwave carouselle
        # todo: should probably stop cursor from moving when hitting a wall
        #print(dir(e))
        #return
        (w, h) = self.GetClientRect()[2:4]
        (x, y) = e.GetPositionTuple()
        (rx, ry)= (x/w, y/h)
        
        if e.LeftDown():
            self.angle_while_grabbing = self.grabbed_angle = expanded_pos_to_angle(rx)
            self.d_angle_while_grabbing = 0
            self.desired_clock_while_grabbing = self.grabbed_pseudoclock = \
                self.__get_current_pseudoclock()
            self.was_playing_before_drag = self.gui_project.is_playing
            self.gui_project.stop_playing()
            self.being_grabbed = True
            
            self.CaptureMouse()    
            self.SetCursor(cursor_collection.get_closed_grab())
            return
        
        if e.LeftIsDown():
            if not self.HasCapture():
                return
            self.angle_while_grabbing = expanded_pos_to_angle(rx)
            self.d_angle_while_grabbing = (self.angle_while_grabbing - self.grabbed_angle)
            self.desired_clock_while_grabbing = self.grabbed_pseudoclock + \
                (self.d_angle_while_grabbing / self.clock_factor)
                       
            both_nodes = self.gui_project.path.get_node_by_clock(
                self.desired_clock_while_grabbing,
                rounding='both'
            )
        
            node = both_nodes[0] or both_nodes[1]
            
            self.gui_project.set_active_node(node, modify_path=False)
                
        if e.LeftUp(): #or e.Leaving():
            # todo: make sure that when leaving
            # entire app, things don't get fucked
            if self.HasCapture():
                self.ReleaseMouse()
            self.SetCursor(cursor_collection.get_open_grab())
            self.being_grabbed = False
            self.grabbed_angle = None
            self.grabbed_pseudoclock = None
            self.angle_while_grabbing = None
            self.d_angle_while_grabbing = None
            self.desired_clock_while_grabbing = None
            
            if self.was_playing_before_drag:
                self.gui_project.start_playing()
            
            self.was_playing_before_drag = None
        
        return
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
