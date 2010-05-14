# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.


from .roundings import (Rounding, roundings, LOW, LOW_IF_BOTH,
                        LOW_OTHERWISE_HIGH, HIGH, HIGH_IF_BOTH,
                        HIGH_OTHERWISE_LOW, EXACT, CLOSEST, CLOSEST_IF_BOTH,
                        BOTH)

from .functions import (binary_search, binary_search_by_index)
        
        
class BinarySearchProfile(object):
    def __init__(self, sequence, function, value, searcher=binary_search):
        both = searcher(sequence, function, value, BOTH)
        for rounding in roundings:
            setattr(
                self,
                rounding.__name__,
                make_both_data_into_preferred_rounding(both, function, value,
                                                       rounding)
            )

        self.had_to_compromise = {
            LOW_OTHERWISE_HIGH:
                self(LOW_OTHERWISE_HIGH) is not self(LOW),
            HIGH_OTHERWISE_LOW:
                self(HIGH_OTHERWISE_LOW) is not self(HIGH),
        }
        '''tododoc'''
        
        self.got_none_because_no_item_on_other_side = {
            LOW_IF_BOTH:
                self(LOW_IF_BOTH) is not self(LOW),
            HIGH_IF_BOTH:
                self(HIGH_IF_BOTH) is not self(HIGH),
            CLOSEST_IF_BOTH:
                self(CLOSEST_IF_BOTH) is not self(CLOSEST),
        }
        '''tododoc'''
        
        for d in [self.had_to_compromise,
                  self.got_none_because_no_item_on_other_side]:
            
            for rounding in roundings:
                if rounding not in d:
                    d[rounding] = None
        