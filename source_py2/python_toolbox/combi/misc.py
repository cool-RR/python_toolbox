# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

import math

from python_toolbox import misc_tools
from python_toolbox import math_tools
from python_toolbox import cute_iter_tools

infinity = float('inf')


class MISSING_ELEMENT(misc_tools.NonInstantiable): 
    '''A placeholder for a missing element used in internal calculations.'''
        
        
@misc_tools.limit_positional_arguments(1)
def get_short_factorial_string(number, minus_one=False):
    '''
    Get a short description of the factorial of `number`.
    
    If the number is long, just uses factorial notation. 
    
    Examples:
    
        >>> get_short_factorial_string(4)
        '24'
        >>> get_short_factorial_string(14)
        '14!'
    
    '''
    assert number >= 0 and \
                    isinstance(number, math_tools.PossiblyInfiniteIntegral)
    if number == infinity:
        return "float('inf')"
    elif number <= 10:
        return str(math.factorial(number) - int(minus_one))
    else:
        assert number > 10
        return '%s!%s' % (number, ' - 1' if minus_one else '')
        

    