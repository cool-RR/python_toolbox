# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

import numbers
import collections


infinity = float('inf')


_stirling_caches = []
_n_highest_cache_completed = -1
def stirling(n, k, skip_calculation=False):
    '''
    blocktododoc specify first kind
    '''
    global _n_highest_cache_completed
    if k not in range(n + 1):
        return 0
    if n == k == 0:
        return 1
    if not skip_calculation:
        for current_n in range(_n_highest_cache_completed + 1, n+1):
            try:
                cache = _stirling_caches[current_n]
            except IndexError:
                cache = []
                _stirling_caches.append(cache)
            calculate_up_to = min(k, current_n)
            current_index = len(cache)
            while current_index < calculate_up_to + 1:
                if current_index == 0:
                    cache.append(0)
                elif current_index == current_n:
                    cache.append(1)
                else:
                    cache.append(
                        - (current_n - 1) * stirling(current_n - 1,
                                                     current_index,
                                                     skip_calculation=True) +
                        stirling(current_n - 1, current_index - 1,
                                 skip_calculation=True)
                    )
                
                current_index += 1
            if calculate_up_to == current_n:
                _n_highest_cache_completed = max(
                    _n_highest_cache_completed,
                    current_n
                )
                
                
    return _stirling_caches[n][k]


def abs_stirling(n, k):
    return abs(stirling(n, k))
    
###############################################################################

_shitfuck_cache = {}

def get_sub_counters(counter):
    assert isinstance(counter, nifty_collections.FrozenCounter)
    return {
        nifty_collections.FrozenCounter(
            {key: (value - (key == key_to_reduce)) for key, value in self.items()}
        ) for key_to_reduce in self
    }
    

def shitfuck(k, recurrence_counter):
    from python_toolbox import nifty_collections
    assert isinstance(recurrence_counter, nifty_collections.FrozenCounter)
    levels = []
    current_reccurence_counters = {recurrence_counter}
    while len(levels) < k and any(((k - len(levels) + 1), recurrence_counter)
                                   not in _shitfuck_cache for x in levels[-1]):
        new_level = {}
        for recurrence_counter_ in current_reccurence_counters:
            new_level[recurrence_counter_] = 
            for smaller_recurrence_counter in recurrence_counter_.counters_with_one_removed:
                new_level[(k - len(levels), smaller_recurrence_counter)] += factor
        levels.append(new_level)
    # The last level is calculated. Time to make our way up.
    if len(levels) == k:
        
            
