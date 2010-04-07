from __future__ import division

import wx
import math
import pkg_resources
from garlicsim.general_misc import math_tools
from garlicsim_wx.general_misc import wx_tools
from garlicsim_wx.general_misc import cursor_collection
from garlicsim.general_misc import binary_search
from garlicsim.general_misc import cute_iter_tools

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
        self.snap_point_ratio_well = 1 # 0.4
        
        self.base_drag_radius = 100#50 # in pixels
        self.snap_point_drag_well = \
            self.snap_point_ratio_well * self.base_drag_radius
         # todo: warning, this attribute is not dynamic
            
        self.being_dragged = False
        
        self.grabbed_rev_y = None
        self.grabbed_ratio = None
        self.origin_rev_y_while_dragging = None
        self.snap_points_rry_starts = []
        #self.ratio_while_dragging = None
        #self.d_angle_while_dragging = None
        #self.desired_clock_while_dragging = None
        
        self.set_snap_point(1)
        self.set_snap_point(4)
        self.set_snap_point(-1)
        
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
        # Not optimizing with the sorting for now
        self.snap_points.append(value)
        self.snap_points.sort()
    
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
        return [self._value_to_ratio(value) for value in self.snap_points]
    
    def __make_snap_points_rry_starts(self): # todo: should be named ry?
        
        self.snap_points_rry_starts = []
        snap_point_ratios = self._get_snap_points_as_ratios()
        if not snap_point_ratios:
            return
        assert len(snap_point_ratios) >= 1
        my_i = binary_search.binary_search_by_index(
            snap_point_ratios,
            function=None,
            value=0,
            rounding='low'
        )
        
        first_negative_i = None
        zero_is_snap_point = False
        
        if my_i is None:
            first_positive_i = 0
        else:
            first_positive_i = my_i + 1
        
            if snap_point_ratios[my_i] == 0:
                first_negative_i = my_i - 1
                zero_is_snap_point = True
            else:
                first_negative_i = my_i
                
            
        try:
            assert snap_point_ratios[first_negative_i] < 0
        except (IndexError, TypeError): # TypeError in case it's None
            pass
        
        try:
            assert snap_point_ratios[first_positive_i] > 0
        except IndexError:
            pass
        
                
            
        zero_padding = \
            self.snap_point_drag_well / 2 if zero_is_snap_point else 0

        negative_snap_point_ratios = snap_point_ratios[:first_negative_i+1] \
                                   if first_negative_i is not None else []
        positive_snap_point_ratios = snap_point_ratios[first_positive_i:]
        
        
        
        for (i, ratio) in cute_iter_tools.enumerate(negative_snap_point_ratios,
                                                    reverse_index=True):
            assert ratio < 0 # todo: remove
            padding_to_add = - (i * self.snap_point_drag_well + zero_padding)
            self.snap_points_rry_starts.append(
                ratio * self.base_drag_radius + padding_to_add
            )
        
        for (i, ratio) in enumerate(positive_snap_point_ratios):
            assert ratio > 0 # todo: remove
            padding_to_add = i * self.snap_point_drag_well + zero_padding
            self.snap_points_rry_starts.append(
                ratio * self.base_drag_radius + padding_to_add
            )
        
            
    def __get_snap_points_rry_starts_from_origin(self, rry):
        result = [rry_start for rry_start in self.snap_points_rry_starts
                  if (0 <= rry_start < rry) or (0 >= rry_start > rry)]
        
        # # # # assertion block for debugging. todo: remove it # #
        signs_of_result = [math_tools.sign(rry_start) for rry_start in result]
        signs_set = set(signs_of_result + [math_tools.sign(rry)])
        assert not ((-1 in signs_set) and (1 in signs_set))
        # # # #
        return result
    
        
    
    def __get_n_snap_points_from_origin(self, ratio):
        '''note it returns a float'''
        
        counter = 0.
        
        snap_point_ratios = self._get_snap_points_as_ratios()

        snap_points_between = [s for s in snap_point_ratios
                               if (0 < s < ratio ) or (0 > s > ratio)]

        closest_snap_point = binary_search.binary_search(
            snap_point_ratios,
            function=None,
            value=ratio,
            rounding='closest'
        )

        if abs(closest_snap_point - ratio) < (self.snap_point_ratio_well / 2):
            # Are we inside the well of the closest snap point?
            
            # If so, we'll register it as 0.5 for our counter.
            counter += 0.5
            
            # Also, we need to make sure to remove this snap point from the
            # list. We can't be sure if it was included or not due to the
            # fuzziness of floating numbers, so we do it in a try-except.
            try:
                snap_points_between.remove(closest_snap_point)
            except ValueError:
                pass
        
        counter += len(snap_points_between)
        if any(s == 0 for s in snap_point_ratios):
            # We're substracting 0.5 because the zero-snap-point was already
            # counted as a full 1 when it should only be counted as 0.5.
            counter -= 0.5 
        return counter
    
    #def __raw_map_y_to_ratio(self, y):
        #assert self.being_dragged
        #ratio = (y - self.origin_rev_y_while_dragging) / self.base_drag_radius
        #if abs(ratio) > 1:
            #ratio = math_tools.sign(ratio)
        #return ratio
    
    def __map_y_to_ratio(self, rev_y): # todo: rename to rev_y
        
        rry =  rev_y - self.origin_rev_y_while_dragging
        print rry
        pass
        
        rry_starts_from_origin = \
            self.__get_snap_points_rry_starts_from_origin(rry)
        
        padding_counter = 0
        
        if len(rry_starts_from_origin) > 0:
            if rry_starts_from_origin[0] == 0:
                padding_counter += self.snap_point_drag_well / 2
                rry_starts_from_origin.pop(0)
                
            distance_from_last = abs(rry - rry_starts_from_origin[-1])
            if distance_from_last < self.snap_point_drag_well:
                padding_counter += distance_from_last
                rry_starts_from_origin.pop(-1)
            
            padding_counter += \
                self.snap_point_drag_well * len(rry_starts_from_origin)
        
        new_rry = rry - padding_counter * math_tools.sign(rry)
        assert math_tools.sign(new_rry) == math_tools.sign(rry)
        
        ratio = new_rry / self.base_drag_radius
        if abs(ratio) > 1:
            ratio = math_tools.sign(ratio)
        # print(self.origin_rev_y_while_dragging, rev_y, ratio)
        return ratio
        
    def on_mouse(self, event):
        # todo: maybe right click should give context menu with 'Sensitivity...'
        # todo: make check: if left up and has capture, release capture

        self.Refresh()
        
        (w, h) = self.GetClientSize()
        (x, y) = event.GetPositionTuple()
        
        rev_y = -y        
        '''
        A reversed y reading of the cursor.
        
        This is useful be The standard positive direction of y on the screen is
        downwards, which is the opposite of what we want.
        '''
        
        if event.LeftDown():
            self.being_dragged = True
            self.grabbed_rev_y = rev_y
            self.origin_rev_y_while_dragging = rev_y - \
                (self.base_drag_radius * (self.current_ratio + \
                math_tools.sign(self.current_ratio) * \
                self.snap_point_ratio_well * \
                self.__get_n_snap_points_from_origin(self.current_ratio)))
            
            self.__make_snap_points_rry_starts()
            
            # # # debug, remove # # #
            offset = self.__map_y_to_ratio(self.origin_rev_y_while_dragging)
            assert 0.01 > offset > -0.01 # might not be exactly cause of fuzziness
            if offset != 0.0: print('warning, nonzero offset %s' % offset)
            # # #
            
            self.CaptureMouse()    
            self.SetCursor(cursor_collection.get_closed_grab())
            return
        
        if event.LeftIsDown() and self.HasCapture():
            ratio = self.__map_y_to_ratio(rev_y)
            value = self._ratio_to_value(ratio)
            self.value_setter(value)
            
                
        if event.LeftUp():#
            # todo: make sure that when leaving
            # entire app, things don't get fucked
            if self.HasCapture():
                self.ReleaseMouse()
            self.SetCursor(cursor_collection.get_open_grab())
            self.being_dragged = False
            self.grabbed_rev_y = None
            self.grabbed_ratio = None
            self.origin_rev_y_while_dragging = None
            del self.snap_points_rry_starts[:]
            
            
        return
    
    def __debug_map(self, start=-500, finish=500, step=10):
        return [(i, self.__map_y_to_ratio(i+self.origin_rev_y_while_dragging))
                for i in xrange(start, finish, step)]
        
        

        
        
        
        
        
        