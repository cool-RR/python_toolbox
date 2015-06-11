# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''
Defines the `BinarySearchProfile` class.

See its documentation for more info.
'''

from python_toolbox import misc_tools

from .roundings import (Rounding, roundings, LOW, LOW_IF_BOTH,
                        LOW_OTHERWISE_HIGH, HIGH, HIGH_IF_BOTH,
                        HIGH_OTHERWISE_LOW, EXACT, CLOSEST, CLOSEST_IF_BOTH,
                        BOTH)
from .functions import (binary_search, binary_search_by_index,
                        make_both_data_into_preferred_rounding,
                        _binary_search_both)
        
        
class BinarySearchProfile(object):
    '''
    A profile of binary search results.
    
    A binary search profile allows to access all kinds of aspects of the
    results of a binary search, while not having to execute the search more
    than one time.
    '''
    
    @misc_tools.limit_positional_arguments(4)
    def __init__(self, sequence, value, function=misc_tools.identity_function,
                 both=None):
        '''
        Construct a `BinarySearchProfile`.
        
        `sequence` is the sequence through which the search is made. `function`
        is a strictly monotonic rising function on the sequence. `value` is the
        wanted value.
        
        In the `both` argument you may put binary search results (with the BOTH
        rounding option.) This will prevent the constructor from performing the
        search itself. It will use the results you provided when giving its
        analysis.
        '''

        if both is None:
            both = _binary_search_both(sequence, value, function=function)
        
        self.results = {}
        '''
        `results` is a dict from rounding options to results that were obtained
        using each function.
        '''
        
        for rounding in roundings:
            self.results[rounding] = make_both_data_into_preferred_rounding(
                both, value, function=function, rounding=rounding
            )
        none_count = list(both).count(None)
        
        self.all_empty = (none_count == 2)
        '''Flag saying whether the sequence is completely empty.'''
        
        self.one_side_empty = (none_count == 1)
        '''Flag saying whether the value is outside the sequence's scope.'''
        
        self.is_surrounded = (none_count == 0)
        '''Flag saying whether the value is inside the sequence's scope.'''
            
        self.had_to_compromise = {
            LOW_OTHERWISE_HIGH:
                self.results[LOW_OTHERWISE_HIGH] is not self.results[LOW],
            HIGH_OTHERWISE_LOW:
                self.results[HIGH_OTHERWISE_LOW] is not self.results[HIGH],
        }
        '''
        Dictionary from "otherwise"-style roundings to bool.
        
        What this means is whether the "otherwise" route was taken. See
        documentation of LOW_OTHERWISE_HIGH for more info.
        '''
        
        self.got_none_because_no_item_on_other_side = {
            LOW_IF_BOTH:
                self.results[LOW_IF_BOTH] is not self.results[LOW],
            HIGH_IF_BOTH:
                self.results[HIGH_IF_BOTH] is not self.results[HIGH],
            CLOSEST_IF_BOTH:
                self.results[CLOSEST_IF_BOTH] is not self.results[CLOSEST],
        }
        '''
        Dictionary from "if both"-style roundings to bool.
        
        What this means is whether the result was none because the BOTH result
        wasn't full. See documentation of LOW_IF_BOTH for more info.
        '''
        
        for d in [self.had_to_compromise,
                  self.got_none_because_no_item_on_other_side]:
            
            for rounding in roundings:
                if rounding not in d:
                    d[rounding] = None
        