# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

import numbers
import collections
import itertools

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

def shitfuck(k, recurrence_counter):
    from python_toolbox import nifty_collections
    from python_toolbox import cute_iter_tools
    if not isinstance(recurrence_counter, nifty_collections.FrozenCrateCounter):
        recurrence_counter = \
                       nifty_collections.FrozenCrateCounter(recurrence_counter)
    if k == 1:
        assert recurrence_counter # Works because `FrozenCounter` implements
                                  # `__bool__`.
        return 1
    try:
        return _shitfuck_cache[(k, recurrence_counter)]
    except KeyError:
        pass
    
    levels = []
    current_reccurence_counters = {recurrence_counter}
    while len(levels) < k and current_reccurence_counters:
        k_ = k - len(levels)
        levels.append(
            {recurrence_counter_: recurrence_counter_.get_sub_counters_counter()
             for recurrence_counter_ in current_reccurence_counters
                            if (k_, recurrence_counter_) not in _shitfuck_cache
        })
        current_reccurence_counters = \
                                     set(itertools.chain(*levels[-1].values()))
        
    # The last level is calculated. Time to make our way up.
    for k_, level in enumerate(reversed(levels), (k - len(levels) + 1)):
        if k_ == 1:
            for recurrence_counter_, sub_counters_counter in level.items():
                _shitfuck_cache[(k_, recurrence_counter_)] = \
                                                 recurrence_counter_.n_elements
        else:
            for recurrence_counter_, sub_counters_counter in level.items():
                _shitfuck_cache[(k_, recurrence_counter_)] = sum(
                    (_shitfuck_cache[(k_ - 1, sub_counter)] * factor for
                           sub_counter, factor in sub_counters_counter.items())
                )
    
    return _shitfuck_cache[(k, recurrence_counter)]
        
    


###############################################################################

_catshit_cache = {}

def catshit(k, recurrence_counter):
    from python_toolbox import nifty_collections
    from python_toolbox import cute_iter_tools
    if not isinstance(recurrence_counter, nifty_collections.FrozenCrateCounter):
        recurrence_counter = \
                       nifty_collections.FrozenCrateCounter(recurrence_counter)
    if k == 1:
        assert recurrence_counter # Works because `FrozenCounter` implements
                                  # `__bool__`.
        return 1
    try:
        return _catshit_cache[(k, recurrence_counter)]
    except KeyError:
        pass
    
    levels = []
    current_reccurence_counters = {recurrence_counter}
    while len(levels) < k and current_reccurence_counters:
        k_ = k - len(levels)
        levels.append(
            {recurrence_counter_: recurrence_counter_.get_sub_counters_counter()
             for recurrence_counter_ in current_reccurence_counters
                            if (k_, recurrence_counter_) not in _catshit_cache
        })
        current_reccurence_counters = \
                                     set(itertools.chain(*levels[-1].values()))
        
    # The last level is calculated. Time to make our way up.
    for k_, level in enumerate(reversed(levels), (k - len(levels) + 1)):
        if k_ == 1:
            for recurrence_counter_, sub_counters_counter in level.items():
                _catshit_cache[(k_, recurrence_counter_)] = \
                                                 recurrence_counter_.n_elements
        else:
            for recurrence_counter_, sub_counters_counter in level.items():
                _catshit_cache[(k_, recurrence_counter_)] = sum(
                    (_catshit_cache[(k_ - 1, sub_counter)] * factor for
                           sub_counter, factor in sub_counters_counter.items())
                )
    
    return _catshit_cache[(k, recurrence_counter)]
        
    
            
