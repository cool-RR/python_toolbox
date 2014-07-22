# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

import numbers


infinity = float('inf')


def get_sign(x):
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
    '''
    Convert a number to any base, returning result in tuple.
    
    For example, `convert_to_base_in_tuple(32, base=10)` will be `(3, 2)` while
    `convert_to_base_in_tuple(32, base=16)` will be `(2, 0)`.
    '''
    assert isinstance(number, numbers.Integral)
    assert isinstance(base, numbers.Integral)
    assert base >= 2
    sign_ = get_sign(number)
    if sign_ == 0:
        return (0,)
    elif sign_ == -1:
        raise NotImplementedError
    
    work_in_progress = []
    while number:
        work_in_progress.append(int(number % base))
        number //= base
        
    return tuple(reversed(work_in_progress))
  

        
def restrict_number_to_range(number, low_cutoff=-infinity,
                             high_cutoff=infinity):
    '''
    If `number` is not in the range between cutoffs, return closest cutoff.
    
    If the number is in range, simply return it.
    '''
    if number < low_cutoff:
        return low_cutoff
    elif number > high_cutoff:
        return high_cutoff
    else:
        return number
        
        
def binomial(big, small):
    if big == small:
        return 1
    if big < small:
        return 0
    else:
        return (math.factorial(big) // math.factorial(big - small)
                                                      // math.factorial(small))
    
