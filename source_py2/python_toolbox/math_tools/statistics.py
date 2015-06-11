# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

from __future__ import division

import numbers


infinity = float('inf')
infinities = (infinity, -infinity)


def get_median(iterable):
    '''Get the median of an iterable of numbers.'''
    sorted_values = sorted(iterable)

    if len(iterable) % 2 == 0:
        higher_midpoint = len(iterable) // 2
        lower_midpoint = higher_midpoint - 1
        return (sorted_values[lower_midpoint] +
                sorted_values[higher_midpoint]) / 2
    else:
        midpoint = len(iterable) // 2
        return sorted_values[midpoint]
    
    
def get_mean(iterable):
    '''Get the mean (average) of an iterable of numbers.'''
    sum_ = 0
    for i, value in enumerate(iterable):
        sum_ += value
    return sum_ / (i + 1)

        