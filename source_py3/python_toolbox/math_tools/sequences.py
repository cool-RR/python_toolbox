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

_length_of_recurrent_perm_space_cache = {}

def calculate_length_of_recurrent_perm_space(k, ftt):
    from python_toolbox import nifty_collections
    from python_toolbox import cute_iter_tools
    cache = _length_of_recurrent_perm_space_cache
    if not isinstance(ftt, nifty_collections.FrozenTallyTally):
        ftt = nifty_collections.FrozenTallyTally(ftt)
    if k == 0:
        return 1
    elif k == 1:
        assert ftt
        # (Works because `FrozenCrateCounter` has a functioning `__bool__`,
        # unlike Python's `Counter`.)
        return ftt.n_elements
    try:
        return cache[(k, ftt)]
    except KeyError:
        pass
    
    levels = []
    current_ftts = {ftt}
    while len(levels) < k and current_ftts:
        k_ = k - len(levels)
        levels.append(
            {ftt_: ftt_.get_sub_ftts_for_one_crate_removed()
             for ftt_ in current_ftts
                          if (k_, ftt_) not in cache}
        )
        current_ftts = set(itertools.chain(*levels[-1].values()))
        
    # The last level is calculated. Time to make our way up.
    for k_, level in enumerate(reversed(levels), (k - len(levels) + 1)):
        if k_ == 1:
            for ftt_, sub_ftt_tally in level.items():
                cache[(k_, ftt_)] = ftt_.n_elements
        else:
            for ftt_, sub_ftt_tally in level.items():
                cache[(k_, ftt_)] = sum(
                    (cache[(k_ - 1, sub_ftt)] * factor for
                           sub_ftt, factor in sub_ftt_tally.items())
                )
    
    return cache[(k, ftt)]
        
    


###############################################################################

_length_of_recurrent_comb_space_cache = {}

def calculate_length_of_recurrent_comb_space(k, ftt):
    '''
    blocktodo gotta properly name these two sons of bitches
    '''
    from python_toolbox import nifty_collections
    from python_toolbox import cute_iter_tools
    cache = _length_of_recurrent_comb_space_cache
    if not isinstance(ftt, nifty_collections.FrozenTallyTally):
        ftt = nifty_collections.FrozenTallyTally(ftt)
    if k == 0:
        return 1
    elif k == 1:
        assert ftt
        # (Works because `FrozenCrateCounter` has a functioning `__bool__`,
        # unlike Python's `Counter`.)
        return ftt.n_elements
    try:
        return cache[(k, ftt)]
    except KeyError:
        pass
    
    levels = []
    current_ftts = {ftt}
    while len(levels) < k and current_ftts:
        k_ = k - len(levels)
        levels.append(
            {ftt_: ftt_.get_sub_ftts_for_one_crate_and_previous_piles_removed()
             for ftt_ in current_ftts
                                                    if (k_, ftt_) not in cache}
        )
        current_ftts = set(itertools.chain(*levels[-1].values()))
        
    # The last level is calculated. Time to make our way up.
    for k_, level in enumerate(reversed(levels), (k - len(levels) + 1)):
        if k_ == 1:
            for ftt_, sub_ftts in level.items():
                cache[(k_, ftt_)] = len(sub_ftts)
        else:
            for ftt_, sub_ftts in level.items():
                cache[(k_, ftt_)] = sum(
                    (cache[(k_ - 1, sub_ftt)] for sub_ftt in sub_ftts)
                )
    
    return cache[(k, ftt)]
        
    
            
