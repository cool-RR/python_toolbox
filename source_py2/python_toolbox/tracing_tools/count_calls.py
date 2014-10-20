# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''
Defines the `count_calls` decorator.

See its documentation for more details.
'''

from python_toolbox import decorator_tools


def count_calls(function):
    '''
    Decorator for counting the calls made to a function.

    The number of calls is available in the decorated function's `.call_count`
    attribute.
    
    Example usage:
    
        >>> @count_calls
        ... def f(x):
        ...     return x*x
        ... 
        >>> f(3)
        9
        >>> f(6)
        36
        >>> f.call_count
        2
        >>> f(9)
        81
        >>> f.call_count
        3
    
    '''
    def _count_calls(function, *args, **kwargs):
        decorated_function.call_count += 1
        return function(*args, **kwargs)
    
    decorated_function = decorator_tools.decorator(_count_calls, function)
    
    decorated_function.call_count = 0
    
    return decorated_function

