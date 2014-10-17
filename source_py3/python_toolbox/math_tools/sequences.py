# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

import numbers
import collections
import itertools

infinity = float('inf')


_stirling_caches = []
_n_highest_cache_completed = -1
def stirling(n, k, skip_calculation=False):
    '''
    Calculate Stirling number of the second kind of `n` and `k`.
    
    More information about these numbers:
    https://en.wikipedia.org/wiki/Stirling_numbers_of_the_second_kind
    
    Example:
    
        >>> stirling(3, 2)
        -3
    
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
    '''
    Calculate Stirling number of the first kind of `n` and `k`.
    
    More information about these numbers:
    https://en.wikipedia.org/wiki/Stirling_numbers_of_the_first_kind
    
    Example:
    
        >>> abs_stirling(3, 2)
        3
    
    '''
    return abs(stirling(n, k))
    
