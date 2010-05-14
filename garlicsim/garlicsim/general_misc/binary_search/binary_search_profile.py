# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.


from .roundings import (Rounding, roundings, LOW, LOW_IF_BOTH,
                        LOW_OTHERWISE_HIGH, HIGH, HIGH_IF_BOTH,
                        HIGH_OTHERWISE_LOW, EXACT, CLOSEST, CLOSEST_IF_BOTH,
                        BOTH)

from .functions import (binary_search, binary_search_by_index,
                        make_both_data_into_preferred_rounding)
        
        
class BinarySearchProfile(object):

    
    def __init__(self, sequence, function, value, both=None):

        if both is None:
            both = searcher(sequence, function, value, BOTH)
        
        self.results = {}
        '''tododoc'''
        
        for rounding in roundings:
            self.results[rounding] = \
                make_both_data_into_preferred_rounding(both, function, value,
                                                       rounding)

        self.had_to_compromise = {
            LOW_OTHERWISE_HIGH:
                self.results[LOW_OTHERWISE_HIGH] is not self.results[LOW],
            HIGH_OTHERWISE_LOW:
                self.results[HIGH_OTHERWISE_LOW] is not self.results[HIGH],
        }
        '''tododoc'''
        
        self.got_none_because_no_item_on_other_side = {
            LOW_IF_BOTH:
                self.results[LOW_IF_BOTH] is not self.results[LOW],
            HIGH_IF_BOTH:
                self.results[HIGH_IF_BOTH] is not self.results[HIGH],
            CLOSEST_IF_BOTH:
                self.results[CLOSEST_IF_BOTH] is not self.results[CLOSEST],
        }
        '''tododoc'''
        
        for d in [self.had_to_compromise,
                  self.got_none_because_no_item_on_other_side]:
            
            for rounding in roundings:
                if rounding not in d:
                    d[rounding] = None
        