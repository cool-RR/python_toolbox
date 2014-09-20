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
    
    def add(self, integer_or_integer_segment):
        if isinstance(integer_or_integer_segment, numbers.Integral):
            integer_segment = (int(integer_or_integer_segment),) * 2
            integer = int(integer_or_integer_segment)
            (lower_segment, higher_segment) = binary_search.binary_search(
                self.integer_segments, function=None, value=integer,
                rounding=binary_search.BOTH
            )
            
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
                    
                    
                
        
        
