# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `SnapMap` class.

See its documentation for more info.
'''

from __future__ import division
from python_toolbox import misc_tools


FUZZ = 0.001
'''
The fuzziness of floating point numbers.

If two floats have a distance of less than FUZZ, we may treat them as identical.
'''


class SnapMap(object):
    '''
    Map for deciding which angle the knob will have when mouse-dragging.
    
    
    Here we have three "scales" we are playing in:
    
    1. The "ratio" scale. See documenation on Knob for that one. This controls
       the angle of the knob and the actual value of the final variable.
    
    2. The "y" scale. This is the `y` reading of the mouse on the screen.
    
    3. The "pos" scale. This is a convenient mediator between the first two. It
       is reversed from "y", because on the screen a higher number of y means
       "down", and that's just wrong. Also, it has some translation.
       
    '''
    def __init__(self, snap_point_ratios, base_drag_radius,
                 snap_point_drag_well, initial_y, initial_ratio):
        
        assert snap_point_ratios == sorted(snap_point_ratios)
        
        self.snap_point_ratios = snap_point_ratios
        '''Ordered list of snap points, as ratios.'''
        
        self.base_drag_radius = base_drag_radius
        '''
        The base drag radius, in pixels.
        
        This number is the basis for calculating the height of the area in which
        the user can play with the mouse to turn the knob. Beyond that area the
        knob will be turned all the way to one side, and any movement farther
        will have no effect.
        
        If there are no snap points, the total height of that area will be `2 *
        self.base_drag_radius`.
        '''
        
        self.snap_point_drag_well = snap_point_drag_well
        '''
        The height of a snap point's drag well, in pixels.
        
        This is the height of the area on the screen in which, when the user
        drags to it, the knob will have the value of the snap point.
        
        The bigger this is, the harder the snap point "traps" the mouse.
        '''
        
        self.initial_y = initial_y
        '''The y that was recorded when the user started dragging.'''
        
        self.initial_ratio = initial_ratio
        '''The ratio that was recorded when the user started dragging.'''
        
        self.initial_pos = self.ratio_to_pos(initial_ratio)
        '''The pos that was recorded when the user started dragging.'''
        
        self.max_pos = base_drag_radius * 2 + \
            len(snap_point_ratios) * snap_point_drag_well
        '''The maximum that a pos number can reach before it gets truncated.'''
        
        self._make_snap_point_pos_starts()
            
    
    ###########################################################################
    # # # # Converters:
    ############
    
    def ratio_to_pos(self, ratio):
        '''Convert from ratio to pos.'''
        assert (- 1 - FUZZ) <= ratio <= 1 + FUZZ
        n_snap_points_from_bottom = self._get_n_snap_points_from_bottom(ratio)
        padding = n_snap_points_from_bottom * self.snap_point_drag_well
        distance_from_bottom = ratio - (-1)
        result = padding + distance_from_bottom * self.base_drag_radius
        return result

    def pos_to_y(self, pos):
        '''Convert from pos to y.'''
        assert 0 - FUZZ <= pos <= self.max_pos + FUZZ
        relative_pos = (pos - self.initial_pos)
        return self.initial_y - relative_pos
        # doing minus because y is upside down
    
    def y_to_pos(self, y):
        '''Convert from y to pos.'''
        relative_y = (y - self.initial_y)

        # doing minus because y is upside down
        pos = self.initial_pos - relative_y
        
        if pos < 0:
            pos = 0
        if pos > self.max_pos:
            pos = self.max_pos
        
        return pos
        
        
    def pos_to_ratio(self, pos):
        '''Convert from pos to ratio.'''
        assert 0 - FUZZ <= pos <= self.max_pos + FUZZ
        
        snap_point_pos_starts_from_bottom = [
            p for p in self.snap_point_pos_starts if p <= pos
        ]
        
        padding = 0
        
        if snap_point_pos_starts_from_bottom:

            candidate_for_current_snap_point = \
                snap_point_pos_starts_from_bottom[-1]
        
            distance_from_candidate = (pos - candidate_for_current_snap_point)
            
            if distance_from_candidate < self.snap_point_drag_well:
                
                # It IS the current snap point!
                
                snap_point_pos_starts_from_bottom.remove(
                    candidate_for_current_snap_point
                )
                
                padding += distance_from_candidate
        
        padding += \
            len(snap_point_pos_starts_from_bottom) * self.snap_point_drag_well
        
        
        ratio = ((pos - padding) / self.base_drag_radius) - 1
        
        assert (- 1 - FUZZ) <= ratio <= 1 + FUZZ
        
        return ratio
        
    
    def ratio_to_y(self, ratio):
        '''Convert from ratio to y.'''
        return self.pos_to_y(self.ratio_to_pos(ratio))
    
    def y_to_ratio(self, y):
        '''Convert from y to ratio.'''
        return self.pos_to_ratio(self.y_to_pos(y))
    
    ###########################################################################
    
    def _get_n_snap_points_from_bottom(self, ratio):
        '''Get the number of snap points whose ratio is lower than `ratio`.'''
        raw_list = [s for s in self.snap_point_ratios
                    if -1 <= s <= (ratio + FUZZ)]
        
        if not raw_list:            
            return 0
        else: # len(raw_list) >= 1
            counter = 0
            counter += len(raw_list[:-1])
            last_snap_point = raw_list[-1]
            ratio_in_last_snap_point = (abs(last_snap_point - ratio) < FUZZ)
            if ratio_in_last_snap_point:
                counter += 0.5
            else:
                counter += 1
            return counter    
    
    
    def _make_snap_point_pos_starts(self):
        '''
        Make a list with a "pos start" for each snap point.
        
        A "pos start" is the lowest point, in pos scale, of a snap point's drag
        well.

        The list is not returned, but is stored as the attribute
        `.snap_point_pos_starts`.
        '''
        
        self.snap_point_pos_starts = []
        
        for i, ratio in enumerate(self.snap_point_ratios):
            self.snap_point_pos_starts.append(
                (1 + ratio) * self.base_drag_radius + \
                i * self.snap_point_drag_well
            )
            
    
        
