# todo: if there's a limit to how close snap points can be to each other,
# document it

from __future__ import division
from garlicsim.general_misc import misc_tools

FUZZ = 0.001

class SnapMap(object):
    def __init__(self, snap_point_ratios, base_drag_radius,
                 snap_point_drag_well, initial_y, initial_ratio):
        assert snap_point_ratios == sorted(snap_point_ratios)
        self.snap_point_ratios = snap_point_ratios
        self.base_drag_radius = base_drag_radius
        self.snap_point_drag_well = snap_point_drag_well
        self.initial_y = initial_y
        self.initial_ratio = initial_ratio
        self.initial_pos = self.ratio_to_pos(initial_ratio)
        self.max_pos = base_drag_radius * 2 + \
            len(snap_point_ratios) * snap_point_drag_well
        self._make_snap_point_pos_starts()
            
    
    ###########################################################################
    # # # # Converters:
    ############
    
    def ratio_to_pos(self, ratio):
        assert (- 1 - FUZZ) <= ratio <= 1 + FUZZ
        n_snap_points_from_bottom = self._get_n_snap_points_from_bottom(ratio)
        padding = n_snap_points_from_bottom * self.snap_point_drag_well
        distance_from_bottom = ratio - (-1)
        result = padding + distance_from_bottom * self.base_drag_radius
        return result

    def pos_to_y(self, pos):
        assert 0 - FUZZ <= pos <= self.max_pos + FUZZ
        relative_pos = (pos - self.initial_pos)
        return self.initial_y - relative_pos
        # doing minus because y is upside down
    
    def y_to_pos(self, y):
        relative_y = (y - self.initial_y)

        # doing minus because y is upside down
        pos = self.initial_pos - relative_y
        
        if pos < 0:
            pos = 0
        if pos > self.max_pos:
            pos = self.max_pos
        
        return pos
        
        
    def pos_to_ratio(self, pos):
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
        return self.pos_to_y(self.ratio_to_pos(ratio))
    
    def y_to_ratio(self, y):
        return self.pos_to_ratio(self.y_to_pos(y))
    
    ###########################################################################
    
    def _get_n_snap_points_from_bottom(self, ratio):
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
    
    def _debug_ratio_to_pos(self, step=0.1):
        if step is None: step = 10
        
        return [(i, self.ratio_to_pos(i)) for i in
                misc_tools.frange(-1, 1, step)]
    
    def _make_snap_point_pos_starts(self):
        
        self.snap_point_pos_starts = []
        
        for i, ratio in enumerate(self.snap_point_ratios):
            self.snap_point_pos_starts.append(
                (1 + ratio) * self.base_drag_radius + \
                i * self.snap_point_drag_well
            )
        


if __name__ == '__main__':
    s=SnapMap([-0.3,0,0.5,0.7],100,100,0,0)