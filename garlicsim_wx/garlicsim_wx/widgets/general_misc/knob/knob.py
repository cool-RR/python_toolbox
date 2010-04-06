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
        
        self.recalculation_flag = False        
        
        self.sensitivity = 5
        self.angle_resolution = math.pi / 180 # One degree
        self.current_angle = 0
        self.current_ratio = 0
        self.snap_points = set()
        
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
                   - math.exp(
                       (math.pi * math.sqrt(abs(value))) / \
                       (2 * math.sqrt(self.sensitivity))
                   )
               )

    def _ratio_to_angle(self, ratio):
        return ratio * (math.pi * 5 / 6)
    
    
    def set_snap_point(self, value):
        self.snap_points.add(value)
    
    def remove_snap_point(self, value):
        self.snap_points.remove(value)
        
    def _recalculate(self, event):
        value = self.value_getter()
        self.current_ratio = self._value_to_ratio(value)
        angle = self._ratio_to_angle(self.current_ratio)
        d_angle = angle - self.current_angle
        if d_angle > self.angle_resolution:
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
            self.current_angle,
            (w/2, h/2),
            useMask=True
        )
        