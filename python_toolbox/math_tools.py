# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''This module defines math-related tools.'''

from __future__ import division

import numbers


def sign(x):
    '''Get the sign of a number.'''
    if x > 0:
        return 1
    if x == 0:
        return 0
    assert x < 0
    return -1


def round_to_int(x, up=False):
    '''
    Round a number to an `int`.
    
    This is mostly used for floating points. By default, it will round the
    number down, unless the `up` argument is set to `True` and then it will
    round up.
    
    If you want to round a number to the closest `int`, just use
    `int(round(x))`.
    '''
    rounded_down = int(x // 1)
    if up:
        return int(x) if (isinstance(x, float) and x.is_integer()) \
               else rounded_down + 1
    else:
        return rounded_down
    
def ceil_div(x, y):
    '''Divide `x` by `y`, rounding up if there's a remainder.'''
    return (x // y) + (1 if x % y else 0)


def convert_to_base_in_tuple(number, base):
    assert isinstance(number, numbers.Integral)
    sign_ = sign(number)
    if sign_ == 0:
        return (0,)
    elif sign_ == -1:
        raise NotImplementedError
    
    work_in_progress = []
    while number:
        work_in_progress.append(number % base)
        number //= base
        
    return tuple(reversed(work_in_progress))
  
  