# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

import numbers
import collections

from python_toolbox import decorator_tools
from python_toolbox import comparison_tools
from python_toolbox import binary_search

from .sorted_set import SortedSet

infinity = float('inf')


@comparison_tools.total_ordering    
class IntegerSet(collections.MutableSet, collections.Sequence):
    def __init__(self, iterable):
        self.integer_segments = SortedSet()
        self |= iterable
    
    def _get_interacting_segments(self, new_segment):
        
        # We want to get all the segments that might have any kind of
        # interaction with the new segment. This includes segments that overlap
        # partially or fully with the new segments; segments that contain the
        # new segment or are contained *by* the new segment; and also segments
        # which terminate just one number away from one of the edges of the new
        # segment.
        #
        # There may be any number of such interacting segments. There could be
        # none, there could be one, there could be an unlimited number of them.
        # We need to find them. We do know that if there are any, they'll be
        # contiguous in `self.integer_segments`, so we're looking for the index
        # of the lowest one and the index of the highest one.
        
        lowest_segment_index_candidate = binary_search.binary_search_by_index(
            self.integer_segments, function=lambda low, high: high,
            value=(new_segment[0] - 1), rounding=binary_search.HIGH
        )
        
        # If the segment with index number `lowest_segment_index_candidate` is
        # indeed interacting, then it's the lowest interacting segment. If it's
        # not interacting, then there aren't any interacting segments at all.
        
        if lowest_segment_index_candidate == None:
            return ()
        lowest_segment_candidate = \
                          self.integer_segments[lowest_segment_index_candidate]
        if lowest_segment_candidate[0] <= (new_segment[1] + 1):
            lowest_segment_index = lowest_segment_index_candidate
        else:
            return ()
        
        # At this point we know that there are interacting segments, and we
        # know that `lowest_segment_index` is the index of the lowest one. Time
        # to find the index of the highest one.
        
        highest_segment_index_candidate = binary_search.binary_search_by_index(
            self.integer_segments, function=lambda low, high: low,
            value=(new_segment[1] + 1), rounding=binary_search.LOW
        )
        
        highest_segment_candidate = \
                         self.integer_segments[highest_segment_index_candidate]
        
                       
        highest_segment_index = highest_segment_index_candidate - \
                     (highest_segment_candidate[1] > (new_segment[0] -  1))
          
        
    
    def add(self, integer_or_integer_segment):
        if isinstance(integer_or_integer_segment, numbers.Integral):
            new_segment = (int(integer_or_integer_segment),) * 2
        else:
            assert isinstance(integer_or_integer_segment, collections.Iterable)
            new_segment = tuple(map(int, integer_or_integer_segment))
            assert len(new_segment) == 2
            
            
        1 / 0
        # Checking whether the value exists:
        for low, high in filter(None, (lower_segment, higher_segment)):
            if low <= integer <= high:
                return
            
        ### Consolidating with neighboring segments if possible: ##########
        #                                                                 #
        if (lower_segment is not None) and \
                                       (lower_segment.high == integer - 1):
            if (higher_segment is not None) and \
                                       (higher_segment.low == integer + 1):
                self.integer_segments -= (lower_segment, higher_segment)
                self.integer_segments.add((lower_segment.low,
                                           higher_segment.high))
            else:
                self.integer_segments.discard(lower_segment)
                self.integer_segments.add((lower_segment.low,
                                           lower_segment.high + 1))
            return 
        elif (higher_segment is not None) and \
                                       (higher_segment.low == integer + 1):
            self.integer_segments.discard(higher_segment)
            self.integer_segments.add((higher_segment.low - 1,
                                       higher_segment.high))
            return
        #                                                                  #
        ### Finished consolidating with neighboring segments if possible. ##
        
        self.integer_segments.add((integer, integer))
                
                
            
    
    

