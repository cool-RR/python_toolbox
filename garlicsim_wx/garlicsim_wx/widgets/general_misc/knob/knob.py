from __future__ import division

import wx
import math
import pkg_resources
from garlicsim.general_misc import math_tools
from garlicsim_wx.general_misc import wx_tools

from . import images as __images_package
images_package = __images_package.__name__



class Knob(wx.Panel):
    def __init__(self, parent, getter, setter, *args, **kwargs):
        
        assert 'size' not in kwargs
        
        assert callable(setter) and callable(getter)
        self.value_getter, self.value_setter = getter, setter
        
        wx.Panel.__init__(self, parent, *args, size=(30, 30), **kwargs)
        
        self.original_bitmap = wx.Bitmap(
            pkg_resources.resource_filename(images_package, 'knob.png'),
            wx.BITMAP_TYPE_ANY
        )
        
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.on_mouse)
        
        self.recalculation_flag = False        
        
        self.sensitivity = 25
        self.angle_resolution = math.pi / 180 # One degree
        self.current_angle = 0
        self.current_ratio = 0
        self.snap_points = set()
        self.snap_point_ratio_well = 0.1
        
        self.base_drag_radius = 500 # in pixels
        self.snap_point_drag_well = \
            self.snap_point_ratio_well * self.base_drag_radius
        
        self.being_dragged = False
        
        self.grabbed_y = None
        self.grabbed_ratio = None
        self.origin_y_while_grabbing = None
        #self.ratio_while_dragging = None
        #self.d_angle_while_dragging = None
        #self.desired_clock_while_dragging = None
        
    def _angle_to_ratio(self, angle):
        return angle / (math.pi * 5 / 6)

    def _ratio_to_value(self, ratio):
        #return self.sensitivity * \
               #math_tools.sign(ratio) * \
               #(-2*math.log(math.cos((math.pi*ratio)/2))) / math.pi
        return self.sensitivity * \
               math_tools.sign(ratio) * \
               (4 / math.pi**2) * \
               math.log(math.cos(ratio * math.pi / 2))**2
        
    def _value_to_ratio(self, value):
        return math_tools.sign(value) * \
               (2 / math.pi) * \
               math.acos(
                   math.exp(
                       - (math.pi * math.sqrt(abs(value))) / \
                       (2 * math.sqrt(self.sensitivity))
                   )
               )

    def _ratio_to_angle(self, ratio):
        return ratio * (math.pi * 5 / 6)
    
    
    def set_snap_point(self, value):
        self.snap_points.add(value)
    
    def remove_snap_point(self, value):
        self.snap_points.remove(value)
        
    def _recalculate(self):
        value = self.value_getter()
        self.current_ratio = self._value_to_ratio(value)
        angle = self._ratio_to_angle(self.current_ratio)
        d_angle = angle - self.current_angle
        if abs(d_angle) > self.angle_resolution:
            self.current_angle = angle
            self.Refresh()
        self.recalculation_flag = False
    
    def on_paint(self, event):
        event.Skip()
        if self.recalculation_flag:
            self._recalculate()
        
        dc = wx.PaintDC(self)

        w, h = self.GetClientSize()
        
        wx_tools.draw_bitmap_to_dc_rotated(
            dc,
            self.original_bitmap,
            -self.current_angle,
            (w/2, h/2),
            useMask=True
        )
        
    def _get_snap_points_as_ratios(self):
        return set(self._value_to_ratio(value) for value in self.snap_points)
        
    def __get_n_snap_points_from_origin(self, ratio):
        '''note can return n + 0.5'''
        snap_point_ratios = self._get_snap_points_as_ratios()
        snap_points_between = (s for s in snap_point_ratios if
                               (0 < s < ratio) or (0 > s > ratio))
        result = float(len(list(snap_points_between)))
        if any(s == 0 for s in snap_point_ratios):
            result += 0.5
            
        
    def __make_drag_map(self, origin):
        #snap_point_ratios = self._get_snap_points_as_ratios()

        def _raw_map(y):
            ratio = (y - origin) / self.base_drag_radius
            if abs(ratio) > 1:
                ratio = math_tools.sign(ratio)
            return raw_input
            
        def map(y):
            raw_ratio = _raw_map(y)
            #snap_points_between = [s for s in snap_point_ratios if
                                   #(0 < s < raw_ratio) or (0 > s > raw_ratio)]
            #n_snap_points_between = len(snap_points_between)
            self.__get_n_snap_points_from_origin(raw_ratio)
            
            
        pass
        
    def on_mouse(self, event):
        # todo: maybe right click should give context menu with 'Sensitivity...'
        # todo: make check: if left up and has capture, release capture

        self.Refresh()
        
        (w, h) = self.GetClientSize()
        (x, y) = e.GetPositionTuple()
        (rx, ry) = (x/w, y/h)
        
        if e.LeftDown():
            self.being_dragged = True
            self.grabbed_y = y
            self.origin_y_while_grabbing = \
                self.current_ratio * self.base_drag_radius + \
                self.snap_point_drag_well * 
            
            
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
        
        
        
        
        
        
        
        
        
        