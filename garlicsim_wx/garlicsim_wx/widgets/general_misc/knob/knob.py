from __future__ import division

import wx
import math
import pkg_resources
from garlicsim.general_misc import math_tools
from garlicsim_wx.general_misc import wx_tools
from garlicsim_wx.general_misc import cursor_collection
from garlicsim.general_misc import binary_search
from garlicsim.general_misc import cute_iter_tools

from snap_map import SnapMap


from . import images as __images_package
images_package = __images_package.__name__



class Knob(wx.Panel):
    # todo future: make key that disables snapping while dragging
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
        
        self.SetCursor(cursor_collection.get_open_grab())
        
        self.recalculation_flag = False        
        
        self.sensitivity = 25
        self.angle_resolution = math.pi / 180 # One degree
        self.current_angle = 0
        self.current_ratio = 0
        self.snap_points = []
        
        self.base_drag_radius = 50#100#50 # in pixels
        self.snap_point_drag_well = 20#100 #20 \
            
         
            
        self.being_dragged = False
        self.snap_map = None

        
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
    
    def _get_snap_points_as_ratios(self):
        return [self._value_to_ratio(value) for value in self.snap_points]
    
    def set_snap_point(self, value):
        # Not optimizing with the sorting for now
        self.snap_points.append(value)
        self.snap_points.sort()
    
    def remove_snap_point(self, value):
        self.snap_points.remove(value)
        
    def recalculate(self):
        value = self.value_getter()
        self.current_ratio = self._value_to_ratio(value)
        angle = self._ratio_to_angle(self.current_ratio)
        d_angle = angle - self.current_angle
        if abs(d_angle) > self.angle_resolution:
            self.current_angle = angle
            self.Refresh()
        self.recalculation_flag = False
    
    def on_paint(self, event):
        '''
        """
        event.Skip()
        
        if self.recalculation_flag:
            self.recalculate()
        """
        dc = wx.PaintDC(self)
        """
        w, h = self.GetClientSize()
        
        wx_tools.draw_bitmap_to_dc_rotated(
            dc,
            self.original_bitmap,
            -self.current_angle,
            (w/2, h/2),
            useMask=True
        )
        """
        gc = wx.GraphicsContext.Create(dc)
        assert isinstance(gc, wx.GraphicsContext)
        #gc.PushState()
        gc.SetPen(wx.Pen(wx.NamedColor('Red'), 20))
        gc.DrawEllipse(5, 5, 5, 5)
        gc.DrawEllipse(5, 5, 5, 5)
        #gc.PopState()
        gc.SetFont(wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT))
        gc.DrawText("anurag", 0, 0)
        '''
        dc = wx.PaintDC(self)
        gc = wx.GraphicsContext.Create(dc)

        gc.SetPen(wx.Pen(wx.NamedColor('Red'), 20))
        gc.DrawEllipse(5,5,2,2)
        gc.DrawEllipse(100,200,500,500)
        
    
        
    def on_mouse(self, event):
        # todo: maybe right click should give context menu with 'Sensitivity...'
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
            
            self.CaptureMouse()    
            self.SetCursor(cursor_collection.get_closed_grab())
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
            self.SetCursor(cursor_collection.get_open_grab())
            self.being_dragged = False
            self.snap_map = None
            
            
        return
    
        
        

        
        
        
        
        
        