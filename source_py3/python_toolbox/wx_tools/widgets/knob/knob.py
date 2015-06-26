# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `Knob` class.

See its documentation for more info.
'''

from __future__ import division

import math

import wx
import pkg_resources

from python_toolbox import math_tools
from python_toolbox import wx_tools
from python_toolbox import binary_search
from python_toolbox import cute_iter_tools
from python_toolbox.wx_tools.widgets.cute_panel import CutePanel

from .snap_map import SnapMap

from . import images as __images_package
images_package = __images_package.__name__


class Knob(CutePanel):
    '''
    A knob that sets a real value between `-infinity` and `infinity`.
    
    (Not really touching infinity.)
    
    By turning the knob with the mouse, the user changes a floating point
    variable.


    There are three "scales" that one should keep in mind when working with
    Knob:
    
    1. The "value" scale, which is the value that the actual final variable
       gets. It spans from `-infinity` to `infinity`.
    
    2. The "angle" scale, which is the angle in which the knob appears on
        the screen. It spans from `(-(5/6) * pi)` to `((5/6) * pi)`.
    
    3. As a more convenient mediator between them there's the "ratio" scale,
       which spans from `-1` to `1`, and is mapped linearly to "angle".
    
    
    The knob has snap points that can be modified with `.set_snap_point` and
    `.remove_snap_point`. These are specified by value.
    '''
    # todo future: make key that disables snapping while dragging
    # todo: consider letting the knob turn just a bit slower near the edges.
    # todo: currently forcing size to be constant, in future allow changing
    def __init__(self, parent, getter, setter, *args, **kwargs):
        '''
        Construct the knob.
        
        `getter` is the getter function used to get the value of the variable.
        `setter` is the setter function used to set the value of the variable.
        
        Note that you can't give a size argument to knob, it is always created
        with a size of (29, 29).
        '''
        
        assert 'size' not in kwargs
        kwargs['size'] = (29, 29)
        
        assert callable(setter) and callable(getter)
        self.value_getter, self.value_setter = getter, setter
        
        CutePanel.__init__(self, parent, *args, **kwargs)
        
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        
        self.original_bitmap = wx_tools.bitmap_tools.bitmap_from_pkg_resources(
            images_package,
            'knob.png'
        )
        
        self.bind_event_handlers(Knob)
        
        self.SetCursor(wx_tools.cursors.collection.get_open_grab())
        
        
        self._knob_house_brush = wx.Brush(wx.Colour(0, 0, 0))
        '''Brush used to paint the circle around the knob.'''
        
        self.current_angle = 0
        '''The current angle of the knob.'''
        
        self.current_ratio = 0
        '''The current ratio of the knob.'''
        
        self.sensitivity = 25
        '''
        The knob's sensitivity.
        
        Higher values will cause faster changes in value when turning the knob.
        '''
        
        self.angle_resolution = math.pi / 180
        '''The minimal change in angle that will warrant a repaint.'''
        
        self.snap_points = []
        '''An ordered list of snap points, specified by value.'''
        
        self.base_drag_radius = 50
        '''
        The base drag radius, in pixels.
        
        This number is the basis for calculating the height of the area in which
        the user can play with the mouse to turn the knob. Beyond that area the
        knob will be turned all the way to one side, and any movement farther
        will have no effect.
        
        If there are no snap points, the total height of that area will be `2 *
        self.base_drag_radius`.
        '''
        
        self.snap_point_drag_well = 20
        '''
        The height of a snap point's drag well, in pixels.
        
        This is the height of the area on the screen in which, when the user
        drags to it, the knob will have the value of the snap point.
        
        The bigger this is, the harder the snap point "traps" the mouse.
        '''
            
        self.being_dragged = False
        '''Flag saying whether the knob is currently being dragged.'''
        
        self.snap_map = None
        '''
        The current snap map used by the knob.
        
        See documentation of SnapMap for more info.
        '''
        
        self.needs_recalculation_flag = True
        '''Flag saying whether the knob needs to be recalculated.'''
        
        self._recalculate()

    
    def _angle_to_ratio(self, angle):
        '''Convert from angle to ratio.'''
        return angle / (math.pi * 5 / 6)

    def _ratio_to_value(self, ratio):
        '''Convert from ratio to value.'''
        return self.sensitivity * \
               math_tools.get_sign(ratio) * \
               (4 / math.pi**2) * \
               math.log(math.cos(ratio * math.pi / 2))**2
        
    def _value_to_ratio(self, value):
        '''Convert from value to ratio.'''
        return math_tools.get_sign(value) * \
               (2 / math.pi) * \
               math.acos(
                   math.exp(
                       - (math.pi * math.sqrt(abs(value))) / \
                       (2 * math.sqrt(self.sensitivity))
                   )
               )

    def _ratio_to_angle(self, ratio):
        '''Convert from ratio to angle.'''
        return ratio * (math.pi * 5 / 6)
    
    def _get_snap_points_as_ratios(self):
        '''Get the list of snap points, but as ratios instead of as values.'''
        return [self._value_to_ratio(value) for value in self.snap_points]
    
    def set_snap_point(self, value):
        '''Set a snap point. Specified as value.'''
        # Not optimizing with the sorting for now
        self.snap_points.append(value)
        self.snap_points.sort()
    
    def remove_snap_point(self, value):
        '''Remove a snap point. Specified as value.'''
        self.snap_points.remove(value)
        
    def _recalculate(self):
        '''
        Recalculate the knob, changing its angle and refreshing if necessary.
        '''
        value = self.value_getter()
        self.current_ratio = self._value_to_ratio(value)
        angle = self._ratio_to_angle(self.current_ratio)
        d_angle = angle - self.current_angle
        if abs(d_angle) > self.angle_resolution:
            self.current_angle = angle
            self.Refresh()
        self.needs_recalculation_flag = False
    
    def _on_paint(self, event):
        '''EVT_PAINT handler.'''
        
        # Not checking for recalculation flag, this widget is not real-time
        # enough to care about the delay.
        
        dc = wx.BufferedPaintDC(self)
        
        dc.SetBackground(wx_tools.colors.get_background_brush())
        dc.Clear()
        
        w, h = self.GetClientSize()
        
        gc = wx.GraphicsContext.Create(dc)

        gc.SetPen(wx.TRANSPARENT_PEN)
        gc.SetBrush(self._knob_house_brush)
        
        assert isinstance(gc, wx.GraphicsContext)
        gc.Translate(w/2, h/2)
        gc.Rotate(self.current_angle)
        gc.DrawEllipse(-13.5, -13.5, 27, 27)
        gc.DrawBitmap(self.original_bitmap, -13, -13, 26, 26)
        
        #gc.DrawEllipse(5,5,2,2)
        #gc.DrawEllipse(100,200,500,500)
        
    def _on_size(self, event):
        '''EVT_SIZE handler.'''
        event.Skip()
        self.Refresh()
      
    def _on_mouse_events(self, event):
        '''EVT_MOUSE_EVENTS handler.'''
        # todo: maybe right click should give context menu with
        # 'Sensitivity...'        
        # todo: make check: if left up and has capture, release capture

        self.Refresh()
        
        (w, h) = self.GetClientSize()
        (x, y) = event.GetPositionTuple()
        
        
        if event.LeftDown():
            self.being_dragged = True
            self.snap_map = SnapMap(
                snap_point_ratios=self._get_snap_points_as_ratios(),
                base_drag_radius=self.base_drag_radius,
                snap_point_drag_well=self.snap_point_drag_well,
                initial_y=y,
                initial_ratio=self.current_ratio
            )
            
            self.SetCursor(wx_tools.cursors.collection.get_closed_grab())
            # SetCursor must be before CaptureMouse because of wxPython/GTK
            # weirdness
            self.CaptureMouse()
            
            return
        
        if event.LeftIsDown() and self.HasCapture():
            ratio = self.snap_map.y_to_ratio(y)
            value = self._ratio_to_value(ratio)
            self.value_setter(value)
            
                
        if event.LeftUp():
            # todo: make sure that when leaving
            # entire app, things don't get fucked
            if self.HasCapture():
                self.ReleaseMouse()
            # SetCursor must be after ReleaseMouse because of wxPython/GTK
            # weirdness
            self.SetCursor(wx_tools.cursors.collection.get_open_grab())
            self.being_dragged = False
            self.snap_map = None
            
            
        return
    
        

        
        
        