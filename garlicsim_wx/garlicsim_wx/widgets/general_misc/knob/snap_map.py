# todo: if there's a limit to how close snap points can be to each other,
# document it

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
        #self._make_snap_point_pos_starts()
            
    
    ###########################################################################
    # # # # Converters:
    ############
    
    def ratio_to_pos(self, ratio):
        n_snap_points_from_bottom = self._get_n_snap_points_from_bottom(ratio)
        padding = n_snap_points_from_bottom * self.snap_point_drag_well
        distance_from_bottom = ratio - (-1)
        result = padding + distance_from_bottom * self.base_drag_radius
        return result

    def pos_to_y(self, pos):
        relative_pos = (pos - self.initial_pos)
        return self.initial_y - relative_pos
        # doing minus because y is upside down
    
    def y_to_pos(self, y):
        relative_y = (y - self.initial_y)
        return self.initial_pos - relative_y
        # doing minus because y is upside down
        
    def pos_to_ratio(self, pos):
        pass
    
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
            self.snap_point_pos_starts.append(
                ratio * self.base_drag_radius + padding_to_add
            )
        
        for (i, ratio) in enumerate(positive_snap_point_ratios):
            assert ratio > 0 # todo: remove
            padding_to_add = i * self.snap_point_drag_well + zero_padding
            self.snap_point_pos_starts.append(
                ratio * self.base_drag_radius + padding_to_add
            )
    
    def pos_to_ratio(self, pos):
        pass

if __name__ == '__main__':
    s=SnapMap([-0.3,0,0.5,0.7],100,100)