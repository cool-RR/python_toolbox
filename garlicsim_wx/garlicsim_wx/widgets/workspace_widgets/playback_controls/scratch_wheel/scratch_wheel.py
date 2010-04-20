# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
tododoc
'''

from __future__ import division

import wx
import math
import time

import garlicsim, garlicsim_wx
from garlicsim_wx.widgets import WorkspaceWidget
from garlicsim_wx.general_misc import cursor_collection
from garlicsim_wx.general_misc import thread_timer
from garlicsim_wx.general_misc import emitters
from garlicsim_wx.general_misc.flag_raiser import FlagRaiser

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

def expanded_angle_to_pos(angle):
    pos = 1 - (angle / (-math.pi))
    return (pos - 0.1) / 0.8
    

#def angle_to_pos(angle):
#    return (1 + math.cos(-angle)) / 2


class ScratchWheel(wx.Panel):
    # todo: This shit needs to get redrawed often enough to see the wheel move
    # when playing
    # todo: Add simple motion blur when moving fast.
    def __init__(self, parent, gui_project, *args, **kwargs):
        
        if 'style' in kwargs:
            kwargs['style'] |= wx.SUNKEN_BORDER
        else:
            kwargs['style'] = wx.SUNKEN_BORDER
            
        wx.Panel.__init__(self, parent, *args, **kwargs)
        
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.on_mouse_event)
        self.Bind(wx.EVT_IDLE, self.on_idle)
        self.Unbind(wx.EVT_ERASE_BACKGROUND) # Good or bad?
        
        self.SetCursor(cursor_collection.get_open_grab())
        
        self.gui_project = gui_project
        
        assert isinstance(self.gui_project, garlicsim_wx.GuiProject)
        
        self.speed_function = lambda x: 20 * x ** 4
        
        self.n_lines = 15
        
        self.line_width = 20

        self.frame_number_that_should_be_drawn = 0
        
        self.current_frame_number = -1
        # Set to -1 to make sure first drawing won't fuck up
        
        self.image_size = images.get_image_size()
        
        self.clock_factor = 0.05 # todo: maybe rename
        
        self.being_dragged = False
        
        self.grabbed_angle = None
        self.grabbed_pseudoclock = None
        self.angle_while_dragging = None
        self.d_angle_while_dragging = None
        self.desired_clock_while_dragging = None
        
        self.velocity_tracking_period = 1#100
        self.last_tracked_time_and_angle = (0, 0)
        self.current_velocity_estimate = 0
        '''
        units of radian per second, and that's a real world second, not in the
        simulation.
        '''
        self.velocity_for_maximal_motion_blur = 10
        self.current_motion_blur_bitmap = None
        self.velocity_time_sampling_minimum = 0.05
        
        self.was_playing_before_drag = None
            
        self.motion_blur_update_timer = thread_timer.ThreadTimer(self)
        self.Bind(thread_timer.EVT_THREAD_TIMER,
                  self.on_motion_blur_update_timer,
                  self.motion_blur_update_timer)
        
        # I don't think ThreadTimer should be used here. But for some reason
        # wx.Timer didn't work.
        
        self.recalculation_flag = False
        
        self.needs_recalculation_emitter = \
            self.gui_project.emitter_system.make_emitter(
                inputs=(
                    self.gui_project.pseudoclock_changed_emitter,
                    self.gui_project.active_node_changed_emitter # todo: needed?
                ),
                outputs=(
                    FlagRaiser(self, 'recalculation_flag'),
                    # todo: currently we refresh, not good. if it's the same
                    # bitmap it'll be wasteful to refresh.
                    # update: I spoke with Andrea about this. He said something
                    # about OnInternalIdle, but it didn't work out (April 10th,
                    # 2010).                    
                ),
                name='needs_recalculation_emitter',
            )
        
        
        self.needs_recalculation_emitter.emit()

        
    def get_current_angle(self):
        return self.__get_current_pseudoclock() * self.clock_factor
    
    def __get_current_pseudoclock(self): 
        gui_project = self.gui_project
        
        if gui_project is None or gui_project.active_node is None:
            return 0
        
        active_node = self.gui_project.active_node
        
        if self.being_dragged is True:
            
            
            if active_node.parent is None or len(active_node.children) == 0:
                return active_node.state.clock
            else:
                clock = self.desired_clock_while_dragging
                if clock < self.gui_project.path[0].state.clock:
                    return self.gui_project.path[0].state.clock
                elif clock > self.gui_project.path[-1].state.clock:
                    return self.gui_project.path[-1].state.clock
                else:
                    return clock
        
        elif gui_project.is_playing:
            return gui_project.simulation_time_krap or \
                   active_node.state.clock
        else:
            return active_node.state.clock
                    
    def _recalculate(self):
        angle = self.get_current_angle()
        frame_number = int(
            ((angle % ((2/3) * math.pi)) / (2 * math.pi)) * 3 * images.N_FRAMES
        )
        if frame_number == images.N_FRAMES:
            frame_number =- 1
        
        self.frame_number_that_should_be_drawn = frame_number        
        
        self.__update_motion_blur_bitmap()
        
        self.recalculation_flag = False
    
    def __update_motion_blur_bitmap(self):

        current = (time.time(), self.get_current_angle())
        last = self.last_tracked_time_and_angle

        d_time = current[0] - last[0]
        d_angle = current[1] - last[1]
        
        if d_time < self.velocity_time_sampling_minimum:
            return
            # This protects us from two things: Having a grossly inaccurate
            # velocity reading because of tiny sample, and having a division by
            # zero.
        
        self.current_velocity_estimate = velocity = d_angle / d_time

        r_velocity = velocity / self.velocity_for_maximal_motion_blur

        alpha = min(abs(r_velocity), 1)
        
        alpha = min(alpha, 0.8)
        # I'm limiting the alpha, still want to see some animation
        
        new_motion_blur_image = images.get_blurred_gear_image_by_ratio(alpha)
        
        self.current_motion_blur_bitmap = new_motion_blur_image
        
        if new_motion_blur_image is not \
           images.get_blurred_gear_image_by_ratio(0):
            # We have a non-zero visible motion blur
            
            self.motion_blur_update_timer.Start(30)
        
        else:
            
            self.motion_blur_update_timer.Stop()
            
        self.last_tracked_time_and_angle = current
            
    def on_paint(self, event):
        # todo: optimization: if motion blur is (rounded to) zero, don't draw
        event.Skip()
        
        if self.recalculation_flag:
            self._recalculate()
            
        bw, bh = self.GetWindowBorderSize()
        
        ox, oy = ((4 - bw) / 2 , (4 - bh) / 2)
        
        bitmap = images.get_image(self.frame_number_that_should_be_drawn)
        dc = wx.PaintDC(self)
        dc.DrawBitmap(bitmap, ox, oy)
        dc.DrawBitmap(self.current_motion_blur_bitmap, ox, oy, useMask=True)
        # todo: Is the way I draw the bitmap the fastest way?
        self.current_frame_number = self.frame_number_that_should_be_drawn
            
    def on_mouse_event(self, e):
        # todo: possibly do momentum, like in old shockwave carouselle.
        # todo: right click should give context menu with 'Sensitivity...' and
        # 'Disable'
        # todo: make check: if left up and has capture, release capture

        self.Refresh()
        
        (w, h) = self.GetClientSize()
        (x, y) = e.GetPositionTuple()
        (rx, ry) = (x/w, y/h)
        
        if e.LeftDown():
            self.angle_while_dragging = self.grabbed_angle = expanded_pos_to_angle(rx)
            self.d_angle_while_dragging = 0
            self.desired_clock_while_dragging = self.grabbed_pseudoclock = \
                self.__get_current_pseudoclock()
            self.was_playing_before_drag = self.gui_project.is_playing
            self.gui_project.stop_playing()
            self.being_dragged = True
            
            self.CaptureMouse()    
            self.SetCursor(cursor_collection.get_closed_grab())
            return
        
        if e.LeftIsDown():
            if not self.HasCapture():
                return
            self.angle_while_dragging = expanded_pos_to_angle(rx)
            self.d_angle_while_dragging = (self.angle_while_dragging - self.grabbed_angle)
            self.desired_clock_while_dragging = self.grabbed_pseudoclock + \
                (self.d_angle_while_dragging / self.clock_factor)
                       
            both_nodes = self.gui_project.path.get_node_by_clock(
                self.desired_clock_while_dragging,
                rounding='both'
            )
        
            node = both_nodes[0] or both_nodes[1]

            self.gui_project.set_active_node(node, modify_path=False)
            self.gui_project.pseudoclock_changed_emitter.emit()
            # todo: gui_project should have method to change pseudoclock, so
            # it'll change the active node itself and we won't need to call any
            # event. this method should also be used in __play_next.
            
            if list(both_nodes).count(None) == 1: # Means we got an edge node
                edge_clock = node.state.clock
                direction = -1 if node is both_nodes[0] else 1
                # direction that we bring back the cursor to if it goes too far
                d_clock = (edge_clock - self.grabbed_pseudoclock)
                d_angle = d_clock * self.clock_factor
                edge_angle = self.grabbed_angle + d_angle
                edge_rx = expanded_angle_to_pos(edge_angle)
                edge_x = edge_rx * w
                is_going_over = \
                    (edge_x - x > 0) if direction == 1 else (edge_x - x < 0)
                if is_going_over:
                    self.WarpPointer(edge_x, y)
            
                
        if e.LeftUp(): #or e.Leaving():
            # todo: make sure that when leaving
            # entire app, things don't get fucked
            if self.HasCapture():
                self.ReleaseMouse()
            self.SetCursor(cursor_collection.get_open_grab())
            self.being_dragged = False
            self.grabbed_angle = None
            self.grabbed_pseudoclock = None
            self.angle_while_dragging = None
            self.d_angle_while_dragging = None
            self.desired_clock_while_dragging = None
            
            if self.was_playing_before_drag:
                self.gui_project.start_playing()
            
            self.was_playing_before_drag = None
            
        return



    def on_size(self, event):
        self.Refresh()
        if event is not None:
            event.Skip()
    
    def on_motion_blur_update_timer(self, event):
        self.recalculation_flag = True
        self.Refresh()
            
    def on_idle(self, event): # todo: kill this
        if self.current_motion_blur_bitmap != images.get_blurred_gear_image(0):
            self.Refresh()
